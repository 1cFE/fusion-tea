# Divertor peak-load transfer: bounded external research

[AGENT] Result: the admitted evidence supports explicit heat destinations and a reference-case equivalent area. It does not establish a quantitative Stellaris machine-size transfer law or independently identify physical wetted area and spatial peaking. Acquisition returned `REGISTERED`; this is a useful source with a bounded geometry gap, not a native `BOUNDED_NEGATIVE`.

## Scope and premise correction

[INHERITED: research-brief.md] Request REQ-DIV-001 asks whether geometry, capture and concentration support transfer beyond fixed-target load normalization. The brief's word “non-resonant” conflicts with the primary source: Stellaris §2.6 describes a resonant 4/4 island chain and plates intersecting it. The coordinator was notified and directed this reading to the represented island divertor. No non-resonant conclusion is made. The sealed hold-out protocol was read before fetching; no barred source was opened. No model, package, study, insight registry or goal trail was changed.

## Source record and acquisition

- [INHERITED: source registry] Existing primary: Lion et al., Stellaris design paper, DOI 10.1016/j.fusengdes.2025.114868. Registered in `knowledge/SOURCE_INDEX.md:179`; source location `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/`. Both original renders `work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p14_divertor.png` and `stellaris_p15_divertor.png` were viewed directly. The iter-01 extraction provides navigable §2.6 text at `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:1080` onward; its tables are not independent witnesses.
- [INHERITED: native registration] New primary: Veksler, Bader, Frerichs and Paul, *Stellarator island divertor shape optimization for reduced peak heat fluxes*, arXiv:2602.24049v2, 17 July 2026. Registered full HTML and extraction: `knowledge/sources/stellarator_island_divertor_shape_optimization_for_reduced/`. Source/raw SHA256 `d790b9caba27cba49f917754522da88b4d202a2bdeb560de5bd1a62224fccfcf`; extract SHA256 `402242eaad6cbbcf225a8c70e486a7d0057dad8c1125b284b8323ba8b084c902`. Citations below use this local capture, not web triage.
- [AGENT] Existing local research checked: `knowledge/research/pending/20260911-170548_step-divertor-exhaust-proxy.md` already distinguishes a tokamak P_sep/R proxy from target heat flux. It does not close this gap, and its unregistered STEP PDF is not used as authority here.
- [INHERITED: native run] Request: `knowledge/research/requests/REQ-DIV-001.json`. Run: `knowledge/research/requests/runs/REQ-DIV-001/20260916T053614233251/`; authoritative result: `return.json`. Two logged searches and two registration attempts stayed within six searches/two captures. The first capture failed on sandbox DNS. The approved network retry registered the same URL. The native return retains the failed attempt in `queued[]` and reports `limit_reached: null` despite closure with adequacy `limit_reached`; the retry success resolves that acquisition obstacle, but the historical receipt and computed return are preserved. No additional capture was attempted. The Davies/HSX design-method candidate was not selected within this budget; its MPG triage fetch returned 403. Its content is not cited. The run's REGISTERED class establishes acquisition, not adequacy of a geometry law.

## What the original Stellaris pages establish

[INHERITED: Stellaris original p.15] The assumed absorbed heating is 500 MW and total radiated fraction is 90%, leaving 50 MW non-radiated. Density is 10¹⁹ m⁻³ in both transport cases. The page pairs the following values explicitly; “respectively” connects each capture fraction to its own peak:

| Case | LCFS temperature | Perpendicular diffusivity | Target capture | Peak target flux |
|---|---|---|---|---|
| Lower parallel/perpendicular transport | 100 eV | 3 m²/s | 97% | 5 MW/m² |
| Higher parallel/perpendicular transport | 200 eV | 1 m²/s | 99% | 9.5 MW/m² |

[INHERITED: Stellaris original p.15] The higher perpendicular transport broadens the wetted footprint, lowers target heat flux and sends more heat to the first wall. Figure 25's approximately 200 mm strike width belongs to the pessimistic 200 eV/1 m²/s heat-load pattern. This width does not supply a total wetted area, target length or spatial peaking factor. The source's 10 MW/m² figure is an adopted steady-state design threshold. Transients, erosion, neutral compression, recycling and ash removal remain outside the thermal demonstration.

[INHERITED: Stellaris original p.14] Plate positioning first captures the SOL power, then plate length is optimized against heat flux while minimizing plate area. Larger plate area absorbs breeding-relevant neutrons. Plates are toroidally discontinuous, and their intersection with the island chain depends on magnetic geometry and bootstrap-current control. Those statements give design mechanisms and costs; they do not state an exponent linking target area or peak heat flux to major radius.

## Supported conservation and reference reconstruction

[AGENT] Let P_nr be the source's non-radiated load before interception, c the target capture fraction, P_t = c P_nr the captured target power, and P_other = (1-c) P_nr the remaining non-radiated power. The source identifies increased first-wall loading when capture falls, but supplies no resolved non-target deposition map. Report that destination as uncaptured non-radiated power unless a separately justified wall model distributes it. Radiation remains a separate destination of the same absorbed heating.

[AGENT] A diagnostic area equivalent is A_eq = P_t/q_peak = c P_nr/q_peak. It is the area that would carry all captured power if loaded uniformly at the peak. The source does not report this as physical wetted area. The two reference reconstructions are:

| Case | Captured target power | Uncaptured non-radiated power | A_eq |
|---|---|---|---|
| 97% / 5 MW/m² | 48.5 MW | 1.5 MW | 9.7 m² |
| 99% / 9.5 MW/m² | 49.5 MW | 0.5 MW | 5.2105263158 m² |

[AGENT] For a chosen physical wetted domain with area A_w and nonnegative heat flux, define F = q_peak/(P_t/A_w). Then q_peak = F c P_nr/A_w and A_eq = A_w/F. This is an identity with a stated domain, not a new empirical transfer law. Peak and integrated power identify only A_w/F. Infinitely many area/peaking pairs reproduce each source case. No separate power-sharing split between targets is identified by these aggregate values.

[AGENT] Holding each paired case's c and A_eq fixed gives q_peak = q_ref P_nr/P_nr,ref, exactly the existing fixed-geometry normalization. Multiplying that result by c again would double count interception. Dividing the two cases' equivalent areas does not measure geometry growth: the source changes transport while retaining the proposed target arrangement. Neither a free capture fraction nor a free A_eq is a supported design improvement.

## What the new geometry paper adds

[INHERITED: registered Veksler et al., output.md:90, 140, 211, 224, 256] Geometry optimization jointly considers target peak flux and power missing the plasma-facing plates. Its fixed-equilibrium simulations show reduced peaks with broader transport, but also increased wall interception. Section 3.4 gives a heat-width relation proportional to sqrt(D L_c/C_s) for constant connection length; the diffusivity scan departs from this relation when wall interception exceeds 5% in those simulations. That 5% is a case observation, not a Stellaris acceptance criterion. Section 4 excludes cooling/support space, manufacturing/alignment tolerances and neutral/core-contamination constraints, and calls for higher-fidelity validation.

[AGENT] This supports retaining captured and uncaptured power together when assessing peak reduction. It does not supply Stellaris connection length, physical area, per-target power shares, a radius exponent or a validated map from machine size to the deposition pattern. The source's diffusivity convention also needs reconciliation before implementing its width equation: §2.2 uses a time-based diffusion coefficient, while §3.4 discusses an artificial coefficient with units of length. This report does not transplant that coefficient or equation numerically.

## Consequence for this goal

[AGENT] A conservative extension can expose capture, uncaptured load and case-derived A_eq while preserving the present reference-normalized peak and its paired source cases. It should carry an explicit status that physical area, peaking and size transfer remain unresolved. Improved geometry requires a specified target and magnetic geometry, transport/deposition calculation, wall destination accounting, and evidence for cooling, supports, tolerances, neutral exhaust and breeding impact. No quantitative geometry lever or relaxed heat-flux threshold is supported by this bounded reading. A future source-backed geometry design can replace this gap; the acquisition here does not close it.

[AGENT] These are research findings for coordinator review. No DI entry or source-derived model policy was approved by this report. Request/run artifacts and the registered source must be committed with the coordinator's round evidence to make the acquisition durable; this delegated reader performed no merge or push.
