# Research run REQ-COOL-R2-METHODS

**Question:** Which independent published equipment correlations permit conceptual installed costing of 8 MPa helium circulators, helium salt heat exchangers and large stainless piping, with year and scope?

**Consumer:** installed-cooling-equipment-costs/T-004  ·  **Request key:** `75a7bf5bc9ab8be3e196c31eacea94c9cd3e62a28f93d7f7b88d38d91d58c0aa`

- searched: `IDAES SSLW costing compressor heat exchanger pressure material cost 2018`
- searched: `Seider compressor centrifugal cost correlation 7.58 0.8 horsepower range 200 30000`
- searched: `NETL capital cost shell tube heat exchanger 10000 square feet 2000 pressure installed piping`
- searched: `site.netl.doe.gov centrifugal compressor capital costing suction pressure high pressure helium`
- searched: `site.osti.gov stainless steel piping cost diameter fabricated installed 316L`
- searched: `site.netl.doe.gov "Weiland" "compressor" "2019" "cost" "pdf"`
- searched: `Seider shell tube heat exchanger correlation area range 150 12000 2013`
- searched: `"stainless" "piping" "cost" "diameter" "nuclear" "DOE"`
- searched: `"helium" "piping" "cost" "kg"`
- candidate https://www.osti.gov/servlets/purl/797810 — **keeper** Pre-fetch metadata conventional NETL chemical equipment; full downloaded text negative for holdout terms; original installed scope and gas process bulk categories.
- candidate https://idaes-pse.readthedocs.io/en/2.7.0/_modules/idaes/models/costing/SSLW.html — **keeper** Pre-fetch original generic chemical equipment code metadata clear; raw Python screened clean. Textbook comparison exposes changed HX constants and hot-side versus shell-pressure assumption.
- candidate https://publications.anl.gov/anlpubs/2018/07/144923.pdf — **keeper** Independent fission report screened clean before reading; nuclear stainless fabrication per mass, explicit large coolant pipe application and separate field scope.
- candidate https://thestemtutor.org/wp-content/uploads/2024/10/Warren-D.-Seider-J.-D.-Seader-Daniel-R.-Lewin-Widagdo-Product-and-Process-Design-Principles-_-Synthesis-Analysis-and-Evaluation-Wiley-2009.pdf — **keeper** Original textbook via public unofficial mirror; whole file screened clean; image-checked compressor equation and motor scope, domains explicit.
