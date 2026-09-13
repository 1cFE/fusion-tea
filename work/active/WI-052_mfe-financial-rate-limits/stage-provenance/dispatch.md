# Stage dispatch evidence

- Spec: `collaboration.spawn_agent`, `fork_turns: none`, task `/root/mfe_financial_item/spec`; brief `spec-brief.md`. The host returned this task name; no raw serialized session log is exposed by this interface.
- Spec after routing answer: `collaboration.spawn_agent`, `fork_turns: none`, task `/root/mfe_financial_item/spec_resolved`; brief `spec-brief.md` plus `spec-routing.md`. Initial spec session interrupted before artifact creation; see routing note.
- Design: `collaboration.spawn_agent`, `fork_turns: none`, task `/root/mfe_financial_item/design`; brief `design-brief.md`. All work after spec isolated to `/tmp/fusion-mfe-financial-rate-limits`, branch `work/mfe-financial-rate-limits`, to avoid concurrent plant-closure production mutation.
- Independent design review: `collaboration.spawn_agent`, `fork_turns: none`, task `/root/mfe_financial_item/review`; brief `review-brief.md`. Native host spawn succeeded after design completion.
- Planning: `collaboration.spawn_agent`, `fork_turns: none`, task `/root/mfe_financial_item/plan`; brief `plan-brief.md`. Owner production hold applies; preparation stops after this stage.
