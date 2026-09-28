# Alternative-point findings log

This continues final-assessment findings F022–F027 and the [LCOE follow-up](../final-assessment/follow-up.md). [OWNER] Asked whether any published ARIES point can be supported by the model and authorized the screen. [AGENT] Checking more than the failed reference point; previous results do not establish universal non-support.

## F028 — None of the screened table entries passes the breeding geometry condition

[AGENT] Seventeen entries in Lyon Tables VII, IX and X, including repeated references, have major radii 7.75–10.90 m. The frozen transport-response table requires exactly 12.7 m major radius and 1.3 m minor radius plus eight other fixed coordinates; it varies blanket thickness only over 0.60–1.00 m. All 17 therefore fail a necessary geometry condition before other unknowns matter. This excludes supported whole-plant prediction in the unchanged model, not physical feasibility. [Static screen](evidence/screen.json), [frozen rules](domain-screen.md).

## F029 — Published field columns and incomplete equipment data prevent a simple alternate-point substitution

[AGENT] Tables VII/IX distinguish axis and peak fields; the seven printed peak entries lie between 11.4 and 16 T, below the selected REBCO model's interval. Table X reports axis field only. No model peak field was replaced by a source value. The alternate tables lack complete per-turn current, turn count and pack/casing definitions, and SiC changes coolant architecture as well as material. [Source review](source-screen.md).

## F030 — Financial accounting can be tested separately, but needs an explicit basis mapping

[AGENT] The published total-capital multiplier already includes construction financing; the model DCF expects overnight capital and applies its own construction-interest factor. A direct capital injection would misidentify those bases. A finance-only reconciliation is possible without coil data, but would test accounting under supplied inputs rather than predict an ARIES plant. [Economic screen](economics-screen.md).

## Independent verification and completion

[AGENT] Independent review accepted the bounded screen with no remaining material findings. Source images, fixed geometry rules and per-point classifications were checked. Domain and combined JSON/CSV replay match exactly; all 1,350 protected files are unchanged. An interim Table X label error was corrected by consuming the source inventory directly before final review. The recommendation is to report the coverage limitation rather than run another unsupported full-plant point. [Review](evidence/review.md).
