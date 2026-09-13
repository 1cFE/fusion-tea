---
date: 2026-09-11
researcher: Codex parent, T-023
topic: STEP divertor exhaust proxy and relevance to Stellaris
tags: [divertor, major-radius, heat-flux, lifetime, STEP]
research_type: domain-source-reading
status: pending
---

# STEP exhaust proxy and the current divertor limit

## Question and authority

[OWNER-VERBATIM] "Related to the divertor heat limit, you should look at ~/1cfe/UKAEA-STEP-CP2502.pdf if you haven't already." This report reads that source under T-023 of `fusion-audit-remediation`. It proposes no model or source approval. The radius repair T-022 remains separately scoped.

## Finding

[AGENT] The paper supports investigating a radius-sensitive exhaust constraint. It does not justify simply increasing the model's 10 MW/m² threshold. Its constrained quantity is power crossing the separatrix divided by major radius, P_sep/R in MW/m. Its relation to target heat flux is an approximate DEMO example, and its STEP scans assume double-null operation. The current stellarator calculation instead predicts peak target heat flux at fixed target geometry and transport. Transferring the tokamak proxy to a stellarator needs an explicit source-supported relation.

## Source and page evidence

[INHERITED: owner-provided local PDF] Jack Foster, Hanni Lux, Samuel Knight, Dan Wolff and Stuart I. Muldrew, *Extrapolating Costs to Commercial Fusion Power Plants*, five-page local copy `/home/reid/1cfe/UKAEA-STEP-CP2502.pdf`, SHA256 `e400b84feb3c4acce8eea045cdaf7a167966149afc93c945aff6978fe8a3164d`. Page numbers below count the first PDF page as page 1. This copy was not found in the existing source index and is not registered or approved by this reading. Publication/version identity beyond the supplied copy has not been independently established.

[AGENT] All five pages were read using the installed PDF skill's single-page markdown extractor. The Table I and Figure 3/4 pages were rendered and directly inspected at 200 DPI to verify units, numbers, legends and mathematical notation. Extracted text and those images are retained in `knowledge/research/pending/step-cp2502-evidence/`. The paper identifies PROCESS v3.0.0, git `536de61792fd064f13421b2e1d9209645a9a7180`, on page 2; no current PROCESS behavior was inferred or executed.

## What it actually measures

| Quantity | Paper evidence | Meaning for this assessment |
|---|---|---|
| P_sep/R limit | Page 4, Figure 4 and adjoining paragraph: scans at 40, 60 and 80 MW/m | A systems-level exhaust proxy, not a heat flux in MW/m² |
| Approximate flux correspondence | Page 4: DEMO example P_sep/R = 20 MW/m corresponds to about 10 MW/m², citing reference 22 | A cited configuration-dependent example, not a universal dimensional conversion |
| Double-null sharing | Page 4: halve the scan proxy limit for each divertor, assuming perfect double-null control | The three scan limits imply 20, 30 and 40 MW/m per divertor under that assumption; this arithmetic does not prove new target-flux limits |
| Divertor allowable fluence | Page 3, Table I: 25.0 MW-yr/m² at both design points; sensitivity 5.0–60.0 | A cumulative exposure/lifetime input, not an instantaneous 25 MW/m² heat-load allowance |
| Replacement sensitivity | Pages 2–4, Section II-C and Figure 3 discussion | Lower allowable fluence increases replacements and operational costs; the paper explicitly says these fluences do not consistently affect plant availability across its scan |

[INHERITED: PDF page 4] The paper explains that the design can keep P_sep/R below its limit by reducing separatrix power, including through greater core radiation, and/or increasing radius. Once further power reduction at a given radius is unavailable, the exhaust constraint forces a larger machine. Figure 4 shows this effect for the three proxy limits. This is a STEP-like spherical-tokamak systems study; it is not a validated stellarator divertor transport calculation.

[INHERITED: PDF pages 1–2] The authors emphasize differential costing and simple integrated systems models. They also distinguish flat-top heating/current-drive demand from gyrotron hardware provided for startup and redundancy. That distinction is consistent with the existing operating-versus-installed procurement separation; the paper supplies no reason to undo that repair.

## Comparison with current model

[INHERITED: source at b9d096f6] `models/library/analyses/mfe_divertor_heat.sysml` defines p_sep as absorbed alpha-plus-operating auxiliary heating minus core radiation. It defines target nonradiated power using the separately held total radiated fraction, then scales the Stellaris reference target peak linearly with that nonradiated power. Those two powers are not interchangeable: the latter also accounts for edge radiation. The same file explicitly holds target geometry and transport fixed and publishes a separate radius-scaled shadow without constraining it.

[INHERITED: source at b9d096f6] `models/designs/stellarator_09/stellarator_plant.sysml`, the WI-047 divertor section, binds total radiated fraction 0.9, reference peak 9.5 MW/m² at 50 MW nonradiated load, threshold 10 MW/m², and radius anchor 12.7 m. Its citations describe the threshold as an adopted steady-state criterion, not irradiated-component lifetime. The original Stellaris case is the basis of those values; this reading does not independently recertify that source.

[AGENT] The STEP paper provides external motivation for studying how geometry and radiation change the exhaust constraint. It does not validate the existing shadow's exact q_peak × R_ref/R scaling: that shadow uses target nonradiated power and assumes target wetted length scales with radius, whereas the paper's proxy uses separatrix power in a tokamak configuration. A constant conversion coefficient or double-null split must not be silently transplanted. Reusing either scan's limit without its geometry/transport assumptions could change which machines appear feasible for an unsupported reason.

[AGENT] No premise needed to bind the current model's one major radius is contradicted. The paper reinforces why a coherent radius producer matters, but the radius repair's frozen comparisons retain their existing fixed-target interpretation. It does expose a relevant open modeling choice for later exhaust/geometry work. The known current-model comment describing the ledger as installed-heating-based is stale (`models/designs/generic_mfe/mfe_plant.sysml`, WI-047 ledger heading); actual operands and the library documentation use operating heat. This observation grants no new model change in T-023.

## Recommendations and limits

- [AGENT] Preserve the current 10 MW/m² adopted threshold until a separately reviewed exhaust model and applicable source basis justify a change. Treat the fixed-target result and radius-scaled alternative as distinct assumptions.
- [AGENT] Assess a geometry-sensitive exhaust contract using separatrix power, core/edge radiation, topology/power sharing and target geometry/transport. The paper's reference 22 is the named follow-up source: Siccinio et al., *Figure of merit for divertor protection in the preliminary design of the EU-DEMO reactor*, Nuclear Fusion 59, 106026 (2019), DOI `10.1088/1741-4326/ab3153`. It is cited here as a follow-up, not as a source already read.
- [AGENT] Keep heat-flux, fluence/lifetime, replacement cost and availability conclusions separate. The paper's own availability limitation prevents using its sensitivity plot as evidence that those mechanisms are consistently coupled.
- [AGENT] Candidate insight for owner review: systems-level P_sep/R limits require configuration-specific translation to peak target flux; a fluence limit is a separate lifetime quantity. No DI entry or accepted source is created by this report.

[AGENT] No relevant existing DI was found that supplies a conflicting divertor proxy or target-flux conversion. This is a pending research reading, not an independent model audit, source approval, new study, feasibility demonstration or acceptance of any goal residual. Source registration/research approval and any implementation disposition remain outstanding.
