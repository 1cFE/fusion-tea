# Research run REQ-MCR-CRYO-01

**Question:** Which admissible primary sources anchor current-lead, thermal-radiation and support-conduction heat loads for a 20 K HTS coil set, and which Stellaris-specific inputs remain missing?

**Consumer:** 20260914-magnet-coil-realism#3  ·  **Request key:** `796ec772c46cf7f6bbe6fe15c6464e91cc1d53b594184e6723a7fb77bb60b265`

- candidate https://trc.nist.gov/cryogenics/materials/G-10%20CR%20Fiberglass%20Epoxy/G10CRFiberglassEpoxy_rev.htm — **keeper** Retry: clean-room material-only topic screen retained; elevated curl retrieves HTML material-property page.
- failed https://cds.cern.ch/record/1026941/files/at-2007-005.pdf — Elevated fetch returns HTML Anubis access challenge instead of PDF; requires accessible primary-author copy or operator retrieval. (queued)
- candidate https://ntrs.nasa.gov/api/citations/20150018118/downloads/20150018118.pdf?attachment=true — **keeper** Retry clean-room screen retained: insulation presentation only; elevated curl verified PDF bytes at /tmp/T004-nasa-insulation.pdf.
- searched: `"HTS Current Leads" "Performance Overview" Ballarino pdf -site:cds.cern.ch`
- candidate https://at-mel-cf.web.cern.ch/resources/Leads_4LB09_last.pdf — **keeper** Same screened CERN lead paper; primary CERN departmental mirror found by query4 across attempts, verified PDF bytes before registration.
- candidate https://at-mel-cf.web.cern.ch/resources/Leads_4LB09_last.pdf — **rejected** Correction: prior verified-bytes note was premature. Elevated curl failed DNS; no PDF existed. Native registration returned precondition_failed without capture. Mirror remains inaccessible in this environment.
- failed https://at-mel-cf.web.cern.ch/resources/Leads_4LB09_last.pdf — Elevated DNS failure for departmental CERN mirror; cern.ch short URL redirects to same unresolved host. No source bytes obtained. (queued)
