# Benchmark acquisition notes

The original IAEA public report URL redirects to a migrated repository landing page. Native registration `iaea_indc_nds_281_fusion_neutron_benchmark_proceedings` captured that landing page despite the local `.pdf` filename. It supplies no benchmark data and must not support quantitative conclusions. The actual PDF is retrieved through its original file link at `https://nds.iaea.org/records/frg42-4y059/files/indc-nds-0281.pdf?download=1`, with separate native registration. This preserves the failed acquisition rather than silently replacing its bytes.

Direct IAEA transfers stalled on the default network route; explicit curl IPv4 retrieval succeeded. The OKTAVIAN readme is also available at `https://www-nds.iaea.org/fendl2/validation/benchmarks/jaerim94014/oktavian/tbr/readme.txt`. Its source figure is absent in the text export. Do not infer missing dimensions from nominal shell thicknesses.
