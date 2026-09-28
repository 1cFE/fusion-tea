# Research run REQ-040-02

**Question:** What clean primary evidence supports separating non-tape material procurement from fabrication in superconducting winding-pack cost, and what defensible bounded accounting model can replace an unsplit conductor-cost multiplier when no procurement split is published?

**Consumer:** WI-040  ·  **Request key:** `cc3be77b105efb975cd8d5b2a450e27a1fb4c3d5741e28b326caf9ac15d30e9d`

- searched: `site:ukaea.github.io/PROCESS superconducting cost winding manufacturing`
- candidate https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs/ — **keeper** Official source implementation; boolean quarantine screen clear; separate TF conductor, winding and case costs.
- candidate https://ukaea.github.io/PROCESS/source/reference/process/data_structure/cost_variables/ — **keeper** Official parameter definitions; quarantine screen clear; establishes historical cost-model year and winding/fixed conductor rate meanings.
- searched: `site.bls.gov CPI historical table 1990 130.7 2024 313.689`
- searched: `site:bls.gov CPI historical table 1990 2024 annual average`
- failed https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm — HTTP 403 on direct fetch; pursuing official Federal Reserve republication of BLS annual CPI as alternative. (queued)
- candidate https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913- — **keeper** Federal Reserve publication of BLS annual CPI; screened clear; explicit general dollar-year conversion for historical winding estimate.
