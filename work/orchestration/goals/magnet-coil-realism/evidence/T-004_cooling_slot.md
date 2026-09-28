# Separate cooling-power slot — 2026-09-15

## Finding

[AGENT] The source code carries separate cooling and cryogenic power inputs, but does not identify the equipment inside the cooling input. This supports separate accounting slots; it does not establish that the 15 MW excludes cryogenic compressors or circulation. The current model already discloses that uncertainty. Goal grounding's description of the relationship as unresolved is therefore accurate, but its account should acknowledge the existing provisional non-cryogenic interpretation.

## Evidence

- External source checkout HEAD is `02543850089be175ea7c28b92a8b2a4184e1637e`, matching the cited source revision. `src/costingfe/data/defaults/steady_state_stellarator.yaml:20` binds `p_cool: 15.0` with only “Cooling power [MW]”; line 24 binds `p_cryo: 0.8` with “Cryogenic power [MW]”. Read directly from that revision with git show.
- `src/costingfe/layers/physics.py:322` adds both inputs to recirculating power. `src/costingfe/types.py:230` calls p_cool cooling power without an equipment list. These code surfaces show separate input slots, not a physical decomposition.
- `models/designs/stellarator_09/stellarator_plant.sysml:1207` at `c8ea5a86` retains 15 MW as non-cryogenic component/room-temperature cooling, cites the source's two slots, and explicitly discloses undocumented upstream composition and possible overlap. The cryogenic direct term is already zeroed because it overlaps the computed cryogenic chain.

Only the source YAML and code surfaces above were inspected. The barred general account-justification document was not opened. No numerical model or package change was made.

## Options for the native design

1. [AGENT] Retain 15 MW as an explicitly assumed, non-cryogenic cooling allowance. Give its equipment boundary in model text and state that the magnitude is inherited rather than independently sized. This preserves the standing model assumption while avoiding a claim that source slot separation proves equipment separation. New cold and warm-intercept refrigeration must all enter the cryogenic chain; none may also be charged to this allowance.
2. [AGENT] Retire the allowance only if admitted evidence establishes that its equipment is fully covered elsewhere, or the owner chooses to omit an unsized residual. Present source-backed equipment accounting first. Two simultaneous source inputs are insufficient evidence for deletion.
3. [AGENT] Rebase the allowance on identified room-temperature pumps/circulators and their duty. This requires capacities, pressure drops and efficiencies that the inspected source code does not provide.

[AGENT] Recommendation: retain the existing allowance provisionally while the source search identifies cryogenic equipment and temperature boundaries. If research does not resolve its composition, surface these options to the owner before claiming goal (a)2 complete. This recommendation supplies no new coefficient and does not settle the missing-input gate.

## Original-page check: lead count — 2026-09-15

[INHERITED: admitted Stellaris raw.pdf, printed p.25, §2.9/Fig.46] The coordinator rendered zero-index page 24 from `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf` and visually checked it in `T-004_stellaris_p25.png`. The text states that coils with the same currents are grouped in series, giving six groups. Fig.46's caption states eight coils with the same current connected in series for one group. The text also explicitly neglects nonzero radial current from redistribution at a joint or the current leads.

[AGENT] The grounding's 96-lead estimate assumes separate terminals on all 48 coils and is not established by this source. One terminal pair per independently powered series group would imply twelve warm-to-cold leads, but the source does not provide a complete terminal/feedthrough design. Twelve is a design option under that assumption, not a printed Stellaris lead count. Circuit topology and physical thermal transitions must be distinguished before choosing a lead heat load. No number has been bound in the model.

## Original-page check: support boundary — 2026-09-15

[INHERITED: admitted Stellaris raw.pdf, printed pp.26–27, §2.10/Fig.48] The coordinator visually checked the support-section pages. The cold structural concept uses AISI 316LN; it consists of coil casings, inter-coil supports and a central ring. Printed p.27 explicitly substitutes root constraints for cryogenic legs and says those legs are not modelled. The retained page image is T-004_stellaris_p27.png. Therefore the paper's cold structural material and pictured frame do not provide a specified warm-to-cold support conduction path. The newly registered G10 material curve is an alternative-material reference, not Stellaris's chosen cold support material or an established leg material. No dimensions were inferred from the schematic.
