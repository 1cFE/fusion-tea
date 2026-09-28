# Common monetary convention

[AGENT] Use USD2025 purchasing-power equivalents for a conditional comparison. Steam captured offers use their source-declared USD2025 basis (`monetary-basis.md`). Multiply explicitly USD2004 ARIES amounts by 321.9/188.9 using the already registered Federal Reserve Bank of Minneapolis annual CPI table. This is a general purchasing-power adjustment, not validated equipment-price escalation.

The coordinator checked the original captured HTML rows as well as the extraction: `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/raw.html:1015` identifies 2004 and 188.9; line 1246 identifies 2025 and 321.9. Matching extracted rows are `output.md:654` and `output.md:801`. Source registry: `knowledge/SOURCE_INDEX.md:572`. No new source was fetched or registered.

[AGENT] The conversion choice remains an economic assumption. Carry equipment-price sensitivity independently; do not interpret CPI as a physical performance or vendor-cost model. The original steam source-file history and its claimed 2019-to-2025 escalation remain unverified. Preserve the captured heat-rejection offer as a fixed purchase despite the original coefficient comment's gross/thermal basis discrepancy; do not reinstate demand-scaled purchasing.
