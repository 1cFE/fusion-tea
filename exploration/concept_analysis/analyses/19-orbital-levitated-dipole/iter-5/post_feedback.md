VERDICT: FINDINGS

### F-1: LCOE skeleton in analysis contradicts model output by ~5×
- **Target:** Section 7 (Rough LCOE skeleton)
- **Category:** analysis
- **Finding:** The Section 7 pessimistic LCOE skeleton estimates ~$2,260/MWh, but the model returns
  $11,800/MWh — a 5× gap. The discrepancy has two sources: (1) the skeleton uses "20% end-to-end
  beaming efficiency" without the DEC proton deceleration stage, while the model correctly uses the
  full 4-stage chain (DEC 57% × TX 15% × beam 89% × rectenna 82% = 3.4% net after recirculating
  loads); (2) the skeleton uses a $20M spacecraft fabrication placeholder while the model derives
  $82.9M from the itemized hardware accounts. The analysis acknowledges both limitations in passing,
  but retains a specific pessimistic dollar figure ($2,260/MWh) that is inconsistent with the model
  in the same section. A reader who computes from the sketch and a reader who reads the model output
  reach different conclusions about the severity of the pessimistic case.
- **Recommendation:** Remove the standalone pessimistic/optimistic LCOE skeleton numbers or
  explicitly mark them as superseded by the model. Replace with a sentence referencing the model
  results directly: pessimistic $11,800/MWh, Optimistic-A $491/MWh, Optimistic-B $261/MWh. If the
  sketch is retained for pedagogical purposes, annotate the efficiency figure as "beaming-only
  sub-chain (excluding DEC)" and note that the full 4-stage model produces $11,800/MWh.
- **Priority:** important

### F-2: Optimistic scenario "50% end-to-end efficiency" is physically unachievable
- **Target:** Section 7 (Modeling Approach Recommendation — scenario structure and sensitivity range)
- **Category:** analysis
- **Finding:** The analysis defines the optimistic scenario as "power beaming at 50% end-to-end
  efficiency (fusion power → delivered AC electricity)" and states a sensitivity sweep range of
  "15–60%." The model's own 4-stage physics contradicts this: maximum achievable full-chain
  efficiency is DEC(65%) × TX(75%, no steering) × beam(89%) × rectenna(82%) ≈ 32% before
  recirculating loads. The model's best scenario (Optimistic-B) achieves 28.1% net. The stated upper
  bound of 60%, and the optimistic scenario's 50%, are not achievable under any near-term technology
  combination — DEC is capped at ~65% (Venetian blind upper bound) and TX without phased-array
  steering is the scenario that achieves ~75% but loses pointing capability. The analysis's own
  "Key Binding Constraints" section (model output) confirms that SPS parity requires ~40% full-chain
  efficiency. Using 50–60% as the optimistic/upper-bound framing overstates achievable performance.
- **Recommendation:** Correct the optimistic scenario efficiency to the model's achievable range.
  Restate: sensitivity sweep range is 15–28% (model-bounded). The optimistic scenario should be
  defined as "transmitter efficiency 75% (no phased-array steering), DEC 65%, yielding ~25–28%
  full-chain net" — which Optimistic-B approximates. Clarify that SPS parity (≤$500/MWh) requires
  simultaneously achieving the upper-bound efficiency AND self-bred He3 AND Starship-era launch, as
  Optimistic-B shows ($261/MWh). Terrestrial fusion parity would require ~35–40% full-chain
  efficiency, which is outside achievable bounds and should be stated explicitly.
- **Priority:** important

### F-3: Competitive efficiency threshold conflates terrestrial and SPS benchmarks
- **Target:** Section 2, hypothesis (c) failure mode; Section 7 competitive benchmarks
- **Category:** analysis
- **Finding:** Section 2 hypothesis (c) states: "If end-to-end efficiency falls below ~20%, the
  delivered-electricity LCOE cannot compete with terrestrial alternatives regardless of fusion Q
  value." But the analysis establishes in Section 7 that the relevant competitive reference for this
  orbital concept is SPS parity ($200–500/MWh), not terrestrial fusion parity ($50–150/MWh). The
  model confirms Optimistic-A achieves $491/MWh at 17.8% full-chain — below the 20% threshold but
  still within SPS parity. The ~20% threshold is approximately the SPS parity threshold under
  optimistic assumptions, not the terrestrial parity threshold (which the model shows is unreachable
  at any achievable efficiency). The failure mode framing in hypothesis (c) uses "terrestrial
  alternatives" as the competitive target, which is inconsistent with the concept's actual
  competitive positioning established later in Section 7.
- **Recommendation:** Revise hypothesis (c) failure mode to: "If end-to-end efficiency falls below
  ~15–20%, the concept cannot achieve SPS parity ($200–500/MWh) even under optimistic fuel and
  launch assumptions. Terrestrial fusion parity ($50–150/MWh) requires ~35–40% full-chain
  efficiency, which is not achievable under any near-term technology combination." This aligns the
  risk statement with the Section 7 competitive positioning and with the model's Optimistic-A/B
  scenario results.
- **Priority:** minor
