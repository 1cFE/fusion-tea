# Research run REQ-040-01

**Question:** What admissible source-backed density, composition and procurement unit-cost basis can price copper jacket, solder, stainless steel and helium in a 20 K stellarator winding pack, distinguishing commercial prices from modeling assumptions?

**Consumer:** WI-040  ·  **Request key:** `ef28869fa766b4fa093e269ff3aa7e3b3561801fdf254746bac6afdf10fc77c8`

- searched: `site.usgs.gov mineral commodity summaries 2025 helium price 2024 copper tin`
- searched: `site.indium.com solder alloy density Sn63 Pb37 8.4`
- searched: `site.nist.gov helium 20 K density 2 MPa`
- searched: `site.onlinemetals.com density copper stainless steel 304`
- searched: `Sn63Pb37 bar solder 1 lb price`
- searched: `site.pubchem.ncbi.nlm.nih.gov copper density 8.96`
- searched: `site.usgs.gov helium 2025 14 cubic meter 15 C 101.325`
- searched: `site.webbook.nist.gov/cgi/fluid.cgi helium`
- candidate https://www.indium.com/products/bar-solder/ — **keeper** Native raw HTML table supplies specific gravity; output.md drops table.
- candidate https://www.rotometals.com/aim-sn63pb37-solder-bar-1/ — **keeper** Retail alloy price retained in native raw HTML.
- candidate https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7440597&Type=IsoTherm&Digits=5&PLow=15&PHigh=20&PInc=5&T=20&RefState=DEF&TUnit=K&PUnit=bar&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm — **keeper** Native captured NIST isotherm supplies state-specific inventory density.
