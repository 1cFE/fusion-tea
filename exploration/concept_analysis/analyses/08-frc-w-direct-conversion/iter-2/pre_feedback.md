VERDICT: FINDINGS

### F-1: CAS27 override is vacuous — library default already zero for this archetype
- **Target:** Section 5b (Override Candidates) and model_setup.py overrides list
- **Category:** model
- **Finding:** The model output shows `CAS27 generic = 0.0` at all scales. The PULSED_FRC archetype, calibrated for Helion-like devices with no blanket, already carries zero for this account. The override `0.05 * generic.costs.cas27 = 0.05 × 0 = 0` has no effect on the LCOE and re-states the library default. The analysis narrative ("near-elimination of the blanket fill account") is misleading when the library default was already zero, not some large positive value that needed reducing.
- **Recommendation:** Disable the CAS27 override in `model_setup.py` and update the Section 5b entry to `enabled: false`. Replace the current rationale with a brief note that the PULSED_FRC library already prices CAS27 at zero for a no-blanket architecture, so no departure is needed. Also check C220101 for the same condition — the model output shows generic C220101 = 0.0 as well; if that is genuinely zero (not a display-rounding artifact of the %.1f format applied to CAS22 sub-accounts), disable that override too.
- **Priority:** minor

---

**Coherence flag note (not a finding):** The pipeline flag reports a C220107 provenance mismatch (model_setup=derived, analysis.md=direct). Reading both current artifacts, both show `provenance: derived` for C220107. The flag does not match current file state and appears to have been generated from an earlier draft. No action needed.
