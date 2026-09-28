---
source: "https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs_2015/"
source_type: "url"
extracted_at: "2026-09-19T01:16:54.917942+00:00"
content_hash_sha256: "16d702b8e8aa78ec0b26aea14f548a0c4a5c9a8041261b36fe946c44c663fd1a"
backend: "trafilatura"
title: "costs_2015"
---

14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618
619
620
621
622
623
624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959
960
961
962
963
964
965
966
967
968
969
970
971
972
973
974
975
976
977
978
979
980
981
982
983
984
985
986
987
988
989
990
991
992
993
994
995
996
997
998
999
1000
1001
1002
1003
1004
1005
1006
1007
1008
1009
1010
1011
1012
1013
1014
1015
1016
1017
1018
1019
1020
1021
1022
1023
1024
1025
1026
1027
1028
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1039
1040
1041
1042
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1056
1057
1058
1059
1060
1061
1062
1063
1064
1065
1066
1067
1068
1069
1070
1071
1072
1073
1074
1075
1076
1077
1078
1079
1080
1081
1082
1083
1084
1085
1086
1087
1088
1089
1090
1091
1092
1093
1094
1095
1096
1097
1098
1099
1100
1101
1102
1103
1104
1105
1106
1107
1108
1109
1110
1111
1112
1113
1114
1115
1116
1117
1118
1119
1120
1121
1122
1123
1124
1125
1126
1127
1128
1129
1130
1131
1132
1133
1134
1135
1136
1137
1138
1139
1140
1141
1142
1143
1144
1145
1146
1147
1148
1149
1150
1151
1152
1153
1154
1155
1156
1157
1158
1159
1160
1161
1162
1163
1164
1165
1166
1167
1168
1169
1170
1171
1172
1173
1174
1175
1176
1177
1178
1179
1180
1181
1182
1183
1184
1185
1186
1187
1188
1189
1190
1191
1192
1193
1194
1195
1196
1197
1198
1199
1200
1201
1202
1203
1204
1205
1206
1207
1208
1209
1210
1211
1212
1213
1214
1215
1216
1217
1218
1219
1220
1221
1222
1223
1224
1225
1226
1227 | ```
class Costs2015(Model):
"""Cost 2015 accounting calculations"""
def __init__(self):
self.outfile = constants.NOUT
def run(self):
"""Cost accounting for a fusion power plant
This routine performs the cost accounting for a fusion power plant.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
self.outfile = self.outfile
# Calculate building costs
self.calc_building_costs()
# Calculate land costs
self.calc_land_costs()
# Calculate tf coil costs
self.calc_tf_coil_costs()
# Calculate fwbs costs
self.calc_fwbs_costs()
# Calculate remote handling costs
self.calc_remote_handling_costs()
# Calculate N plant and vacuum vessel costs
self.calc_n_plant_and_vv_costs()
# Calculate energy conversion system costs
self.calc_energy_conversion_system()
# Calculate remaining subsystems costs
self.calc_remaining_subsystems()
# Calculate total capital cost
self.data.costs_2015.total_costs = (
self.data.costs_2015.s_cost[8]
+ self.data.costs_2015.s_cost[12]
+ self.data.costs_2015.s_cost[20]
+ self.data.costs_2015.s_cost[26]
+ self.data.costs_2015.s_cost[30]
+ self.data.costs_2015.s_cost[33]
+ self.data.costs_2015.s_cost[34]
+ self.data.costs_2015.s_cost[60]
)
# Save as concost, the variable used as a Figure of Merit (M$)
self.data.costs.concost = self.data.costs_2015.total_costs / 1.0e6
# Electrical output (given availability) for a whole year
self.data.costs_2015.mean_electric_output = (
self.data.heat_transport.p_plant_electric_net_mw * self.data.costs.cpfact
)
self.data.costs_2015.annual_electric_output = (
self.data.costs_2015.mean_electric_output * 24.0e0 * 365.25e0
)
# Annual maintenance cost.
self.data.costs_2015.maintenance = (
self.data.costs_2015.s_cost[26] + self.data.costs_2015.s_cost[37]
) * self.data.costs.maintenance_fwbs + (
self.data.costs_2015.s_cost[8]
+ self.data.costs_2015.s_cost[30]
+ self.data.costs_2015.s_cost[33]
+ self.data.costs_2015.s_cost[34]
+ self.data.costs_2015.s_cost[40]
+ self.data.costs_2015.s_cost[42]
+ self.data.costs_2015.s_cost[44]
+ self.data.costs_2015.s_cost[46]
+ self.data.costs_2015.s_cost[47]
+ self.data.costs_2015.s_cost[48]
+ self.data.costs_2015.s_cost[49]
+ self.data.costs_2015.s_cost[50]
+ self.data.costs_2015.s_cost[51]
+ self.data.costs_2015.s_cost[52]
+ self.data.costs_2015.s_cost[53]
+ self.data.costs_2015.s_cost[57]
) * self.data.costs.maintenance_gen
# Levelized cost of electricity (LCOE) ($/MWh)
if self.data.costs_2015.annual_electric_output > 0.00001:
self.data.costs.coe = (
1.0e0 / self.data.costs_2015.annual_electric_output
) * (
self.data.costs_2015.total_costs / self.data.costs.amortization
+ self.data.costs_2015.maintenance
)
# Switch on output if there is a NaN error
if (abs(self.data.costs.concost) > 9.99e99) or (
self.data.costs.concost != self.data.costs.concost
):
self.output()
for i in range(100):
nan_diags = [
self.data.costs_2015.s_label[i],
self.data.costs_2015.s_kref[i],
self.data.costs_2015.s_k[i],
self.data.costs_2015.s_cref[i],
self.data.costs_2015.s_cost[i],
self.data.costs_2015.s_cost_factor[i],
]
nan_diags_str = ",".join(str(x) for x in nan_diags)
logger.info(nan_diags_str)
po.ocmmnt(self.outfile, nan_diags_str)
return
def calc_fwbs_costs(self):
"""Function to calculate the cost of the first wall, blanket and shield
This routine calculates the cost of the first wall, blanket and shield
coils for a fusion power plant based on the costings in the PROCESS costs paper.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(21, 27):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_fwbs
# Enrichment
# Costs based on the number of separative work units (SWU) required
#
# SWU = P V(x_p) + T V(x_t) - F V(x_f)
#
# where V(x) is the value function
#
# V(x) = (1 - 2x)ln((1-x)/x)
# Percentage of lithium 6 in the feed (natural abundance)
feed_li6 = 0.0742e0
# Percentage of lithium 6 in the tail (waste) (75% natural abundance)
tail_li6 = feed_li6 * 0.75e0
# Lithium 6 enrichment cost ($)
self.data.costs_2015.s_label[21] = "Lithium enrichment"
# Zero cost for natural enrichment
if self.data.fwbs.f_blkt_li6_enrichment <= 7.42e0:
self.data.costs_2015.s_cost[21] = 0.0e0
else:
# Percentage of lithium 6 in the product
product_li6 = min(self.data.fwbs.f_blkt_li6_enrichment, 99.99e0) / 100.0e0
# SWU will be calculated for a unit mass of product (P=1)
# Feed to product mass ratio
feed_to_product_mass_ratio = (product_li6 - tail_li6) / (feed_li6 - tail_li6)
# Tail to product mass ratio
tail_to_product_mass_ratio = (product_li6 - feed_li6) / (feed_li6 - tail_li6)
# Calculate value functions
p_v = self.value_function(product_li6)
t_v = self.value_function(tail_li6)
f_v = self.value_function(feed_li6)
# Calculate separative work units per kg
swu = (
p_v + tail_to_product_mass_ratio * t_v - feed_to_product_mass_ratio * f_v
)
# Mass of lithium (kg). Lithium orthosilicate is 22% lithium by mass.
mass_li = self.data.fwbs.m_blkt_li2o * 0.22
# Total swu for lithium in blanket
total_swu = swu * mass_li
# Reference cost for lithium enrichment (2014 $)
self.data.costs_2015.s_cref[21] = 0.1e6
# Reference case of lithium SWU
self.data.costs_2015.s_k[21] = total_swu
self.data.costs_2015.s_kref[21] = 64.7e0
self.data.costs_2015.s_cost[21] = (
self.data.costs_2015.s_cost_factor[21]
* self.data.costs_2015.s_cref[21]
* (self.data.costs_2015.s_k[21] / self.data.costs_2015.s_kref[21])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[22] = "Lithium orthosilicate pebble manufacturing"
# Reference cost of lithium pebble manufacture (2014 $)
self.data.costs_2015.s_cref[22] = 6.5e4
# Scale with mass of pebbles (kg)
self.data.costs_2015.s_k[22] = self.data.fwbs.m_blkt_li2o
self.data.costs_2015.s_kref[22] = 10.0e0
self.data.costs_2015.s_cost[22] = (
self.data.costs_2015.s_cost_factor[22]
* self.data.costs_2015.s_cref[22]
* (self.data.costs_2015.s_k[22] / self.data.costs_2015.s_kref[22])
** self.data.costs.costexp_pebbles
)
self.data.costs_2015.s_label[23] = "Titanium beryllide pebble manufacturing"
# Reference cost of titanium beryllide pebble manufacture (2014 $)
self.data.costs_2015.s_cref[23] = 450.0e6
# Scale with mass of titanium beryllide pebbles (kg)
self.data.costs_2015.s_k[23] = self.data.fwbs.m_blkt_beryllium
self.data.costs_2015.s_kref[23] = 1.0e5
self.data.costs_2015.s_cost[23] = (
self.data.costs_2015.s_cost_factor[23]
* self.data.costs_2015.s_cref[23]
* (self.data.costs_2015.s_k[23] / self.data.costs_2015.s_kref[23])
** self.data.costs.costexp_pebbles
)
self.data.costs_2015.s_label[24] = "First wall W coating manufacturing"
# Reference (PPCS A) first wall W coating cost (2014 $)
self.data.costs_2015.s_cref[24] = 25.0e6
# First wall W coating mass (kg)
self.data.costs_2015.s_k[24] = (
self.data.first_wall.a_fw_total
* self.data.fwbs.fw_armour_thickness
* constants.DEN_TUNGSTEN
)
self.data.costs_2015.s_kref[24] = 29000.0e0
self.data.costs_2015.s_cost[24] = (
self.data.costs_2015.s_cost_factor[24]
* self.data.costs_2015.s_cref[24]
* (self.data.costs_2015.s_k[24] / self.data.costs_2015.s_kref[24])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[25] = (
"Blanket and shield materials and manufacturing"
)
# The cost of making the blanket was estimated for PPCS A.
# This cost includes only manufacturing - not R&D, transport,
# or assembly in the reactor.
# It includes the first wall, blanket and shield, but excludes the breeder
# and multiplier materials.
self.data.costs_2015.s_cref[25] = 317.0e6
# Scale with steel mass in blanket + shield mass
self.data.costs_2015.s_k[25] = (
self.data.fwbs.m_blkt_steel_total + self.data.fwbs.whtshld
)
self.data.costs_2015.s_kref[25] = 4.07e6
self.data.costs_2015.s_cost[25] = (
self.data.costs_2015.s_cost_factor[25]
* self.data.costs_2015.s_cref[25]
* (self.data.costs_2015.s_k[25] / self.data.costs_2015.s_kref[25])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[26] = "Total first wall and blanket cost"
self.data.costs_2015.s_cost[26] = 0.0e0
for j in range(21, 26):
self.data.costs_2015.s_cost[26] += self.data.costs_2015.s_cost[j]
def output(self):
"""Function to output the costs calculations
This routine outputs the costs to output file
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
po.oheadr(
self.outfile,
'Estimate of "overnight" capital cost for a first of kind power plant '
"(2014 M$)",
)
po.oshead(self.outfile, "Buildings (M$)")
for i in range(9):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[i],
i + 1,
self.data.costs_2015.s_cost[i] / 1.0e6,
)
po.oshead(self.outfile, "Land (M$)")
for j in range(9, 13):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[j],
j + 1,
self.data.costs_2015.s_cost[j] / 1.0e6,
)
po.oshead(self.outfile, "TF Coils (M$)")
for k in range(13, 21):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[k],
k + 1,
self.data.costs_2015.s_cost[k] / 1.0e6,
)
po.oshead(self.outfile, "First wall and blanket (M$)")
for l_ in range(21, 27):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[l_],
l_ + 1,
self.data.costs_2015.s_cost[l_] / 1.0e6,
)
po.oshead(self.outfile, "Active maintenance and remote handling (M$)")
self.ocost(
self.outfile,
self.data.costs_2015.s_label[27],
28,
self.data.costs_2015.s_cost[27] / 1.0e6,
)
self.ocost(
self.outfile,
self.data.costs_2015.s_label[28],
29,
self.data.costs_2015.s_cost[28] / 1.0e6,
)
self.ocost(
self.outfile,
self.data.costs_2015.s_label[30],
31,
self.data.costs_2015.s_cost[30] / 1.0e6,
)
po.oshead(self.outfile, "Vacuum vessel and liquid nitrogen plant (M$)")
for n in range(31, 34):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[n],
n + 1,
self.data.costs_2015.s_cost[n] / 1.0e6,
)
po.oshead(self.outfile, "System for converting heat to electricity (M$)")
self.ocost(
self.outfile,
self.data.costs_2015.s_label[34],
35,
self.data.costs_2015.s_cost[34] / 1.0e6,
)
po.oshead(self.outfile, "Remaining subsystems (M$)")
for q in range(35, 61):
self.ocost(
self.outfile,
self.data.costs_2015.s_label[q],
q + 1,
self.data.costs_2015.s_cost[q] / 1.0e6,
)
po.oblnkl(self.outfile)
self.ocost(
self.outfile,
"TOTAL OVERNIGHT CAPITAL COST (M$)",
"(total_costs)",
self.data.costs_2015.total_costs / 1.0e6,
)
self.ocost(
self.outfile,
"Annual maintenance cost (M$)",
"(maintenance)",
self.data.costs_2015.maintenance / 1.0e6,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Net electric output (MW)",
"(p_plant_electric_net_mw)",
self.data.heat_transport.p_plant_electric_net_mw,
"OP ",
)
po.ovarre(
self.outfile, "Capacity factor", "(cpfact)", self.data.costs.cpfact, "OP "
)
po.ovarre(
self.outfile,
"Mean electric output (MW)",
"(mean_electric_output)",
self.data.costs_2015.mean_electric_output,
"OP ",
)
po.ovarre(
self.outfile,
"Capital cost / mean electric output ($/W)",
"",
self.data.costs_2015.total_costs
/ self.data.costs_2015.mean_electric_output
/ 1.0e6,
"OP ",
)
po.ovarre(
self.outfile,
"Levelized cost of electricity ($/MWh)",
"(coe)",
self.data.costs.coe,
"OP ",
)
def calc_building_costs(self):
"""Function to calculate the cost of all buildings.
This routine calculates the building costs for a fusion power plant
based on the costings in the PROCESS costs Paper.
Buildings have a different scaling law, with fixed cost per unit volume.
Cref is therefore now f.Viter.unit_cost
The costs for individual buildings must not be output,
as the same mean cost per unit volume has been used both for light
and for shielded buildings
The exponent =1
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(9):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_buildings
# Power plant admin buildings cost ($)
self.data.costs_2015.s_label[0] = "Admin Buildings"
self.data.costs_2015.s_cref[0] = (
129000.0e0 * self.data.costs.light_build_cost_per_vol
)
self.data.costs_2015.s_cost[0] = (
self.data.costs_2015.s_cost_factor[0] * self.data.costs_2015.s_cref[0]
)
# Tokamak complex excluding hot cell cost ($)
self.data.costs_2015.s_label[1] = "Tokamak Complex (excluding hot cell)"
self.data.costs_2015.s_cref[1] = (
1100000.0e0 * self.data.costs.tok_build_cost_per_vol
)
# ITER cryostat volume (m^3)
self.data.costs_2015.s_k[1] = (
(np.pi * self.data.fwbs.r_cryostat_inboard**2)
* 2.0e0
* self.data.fwbs.z_cryostat_half_inside
)
self.data.costs_2015.s_kref[1] = 18712.0e0
self.data.costs_2015.s_cost[1] = (
self.data.costs_2015.s_cost_factor[1]
* self.data.costs_2015.s_cref[1]
* (self.data.costs_2015.s_k[1] / self.data.costs_2015.s_kref[1])
)
# Neutral beam buildings cost ($)
self.data.costs_2015.s_label[2] = "Neutral beam buildings"
self.data.costs_2015.s_cref[2] = (
28000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with neutral beam wall plug power (MW)
self.data.costs_2015.s_k[2] = self.data.current_drive.pwpnb
self.data.costs_2015.s_kref[2] = 120.0e0
self.data.costs_2015.s_cost[2] = (
self.data.costs_2015.s_cost_factor[2]
* self.data.costs_2015.s_cref[2]
* (self.data.costs_2015.s_k[2] / self.data.costs_2015.s_kref[2])
)
# Cryoplant buildings cost ($)
self.data.costs_2015.s_label[3] = "Cryoplant buildings"
self.data.costs_2015.s_cref[3] = (
130000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with the total heat load on the cryoplant at ~4.5K (kW)
self.data.costs_2015.s_k[3] = self.data.heat_transport.helpow / 1.0e3
self.data.costs_2015.s_kref[3] = 61.0e0
self.data.costs_2015.s_cost[3] = (
self.data.costs_2015.s_cost_factor[3]
* self.data.costs_2015.s_cref[3]
* (self.data.costs_2015.s_k[3] / self.data.costs_2015.s_kref[3])
)
# PF Coil winding building cost ($)
self.data.costs_2015.s_label[4] = "PF Coil winding building"
self.data.costs_2015.s_cref[4] = (
190000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with the radius of the largest PF coil squared (m^2)
self.data.costs_2015.s_k[4] = self.data.pf_coil.r_pf_coil_outer_max**2
self.data.costs_2015.s_kref[4] = 12.4e0**2
self.data.costs_2015.s_cost[4] = (
self.data.costs_2015.s_cost_factor[4]
* self.data.costs_2015.s_cref[4]
* (self.data.costs_2015.s_k[4] / self.data.costs_2015.s_kref[4])
)
# Magnet power supplies and related buildings cost ($)
self.data.costs_2015.s_label[5] = "Magnet power supplies and related buildings"
self.data.costs_2015.s_cref[5] = (
110000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with TF current per coil (MA)
self.data.costs_2015.s_k[5] = (
self.data.tfcoil.c_tf_total / self.data.tfcoil.n_tf_coils
) / 1.0e6
self.data.costs_2015.s_kref[5] = 9.1e0
self.data.costs_2015.s_cost[5] = (
self.data.costs_2015.s_cost_factor[5]
* self.data.costs_2015.s_cref[5]
* (self.data.costs_2015.s_k[5] / self.data.costs_2015.s_kref[5])
)
# Magnet discharge buildings cost ($)
self.data.costs_2015.s_label[6] = "Magnet discharge buildings"
self.data.costs_2015.s_cref[6] = (
35000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with total stored energy in TF coils (GJ)
self.data.costs_2015.s_k[6] = self.data.tfcoil.e_tf_magnetic_stored_total_gj
self.data.costs_2015.s_kref[6] = 41.0e0
self.data.costs_2015.s_cost[6] = (
self.data.costs_2015.s_cost_factor[6]
* self.data.costs_2015.s_cref[6]
* (self.data.costs_2015.s_k[6] / self.data.costs_2015.s_kref[6])
)
# Heat removal system buildings cost ($)
self.data.costs_2015.s_label[7] = "Heat removal system buildings"
# ITER volume of cooling water buildings (m^3)
self.data.costs_2015.s_cref[7] = (
51000.0e0 * self.data.costs.light_build_cost_per_vol
)
# Scale with total thermal power removed from the core (MW)
self.data.costs_2015.s_k[7] = (
self.data.heat_transport.p_plant_primary_heat_mw
+ self.data.heat_transport.p_plant_secondary_heat_mw
)
self.data.costs_2015.s_kref[7] = 880.0e0
self.data.costs_2015.s_cost[7] = (
self.data.costs_2015.s_cost_factor[7]
* self.data.costs_2015.s_cref[7]
* (self.data.costs_2015.s_k[7] / self.data.costs_2015.s_kref[7])
)
# Total cost of buildings ($)
self.data.costs_2015.s_label[8] = "Total cost of buildings"
self.data.costs_2015.s_cost[8] = 0.0e0
for j in range(8):
self.data.costs_2015.s_cost[8] += self.data.costs_2015.s_cost[j]
def calc_land_costs(self):
"""Function to calculate the cost of land for the power plant
Land also uses a unit cost, but area is scaled.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(9, 13):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_land
# Land purchasing cost ($)
self.data.costs_2015.s_label[9] = "Land purchasing"
# ITER Land area (hectares)
ITER_total_land_area = 180.0e0
# ITER Land area for key buildings (hectares)
ITER_key_buildings_land_area = 42.0e0
# ITER buffer land (hectares)
ITER_buffer_land_area = ITER_total_land_area - ITER_key_buildings_land_area
# Scale with area of cryostat (m)
self.data.costs_2015.s_k[9] = np.pi * self.data.fwbs.r_cryostat_inboard**2
self.data.costs_2015.s_kref[9] = 638.0e0
# Cost of land per hectare (2014 $ / ha)
self.data.costs_2015.s_cref[9] = 318000.0e0
# Cost of power plant land (2014 $)
self.data.costs_2015.s_cost[9] = (
self.data.costs_2015.s_cost_factor[9]
* self.data.costs_2015.s_cref[9]
* (
ITER_key_buildings_land_area
* (self.data.costs_2015.s_k[9] / self.data.costs_2015.s_kref[9])
** self.data.costs.costexp
+ ITER_buffer_land_area
)
)
# Land improvement costs ($)
self.data.costs_2015.s_label[10] = "Land improvement"
# Cost of clearing ITER land
self.data.costs_2015.s_cref[10] = 214.0e6
# Scale with area of cryostat (m)
self.data.costs_2015.s_k[10] = np.pi * self.data.fwbs.r_cryostat_inboard**2
self.data.costs_2015.s_kref[10] = 638.0e0
self.data.costs_2015.s_cost[10] = (
self.data.costs_2015.s_cost_factor[10]
* (self.data.costs_2015.s_k[10] / self.data.costs_2015.s_kref[10])
** self.data.costs.costexp
* self.data.costs_2015.s_cref[10]
)
# Road improvements cost ($)
self.data.costs_2015.s_label[11] = "Road improvements"
# Cost of ITER road improvements
self.data.costs_2015.s_cref[11] = 150.0e6
# Scale with TF coil longest dimension
self.data.costs_2015.s_k[11] = (
max(self.data.build.dh_tf_inner_bore, self.data.build.dr_tf_inner_bore)
+ 2.0e0 * self.data.build.dr_tf_inboard
)
self.data.costs_2015.s_kref[11] = 14.0e0
self.data.costs_2015.s_cost[11] = (
self.data.costs_2015.s_cost_factor[11]
* self.data.costs_2015.s_cref[11]
* (self.data.costs_2015.s_k[11] / self.data.costs_2015.s_kref[11])
** self.data.costs.costexp
)
# Total land costs ($)
self.data.costs_2015.s_label[12] = "Total land costs"
self.data.costs_2015.s_cost[12] = 0.0e0
for j in range(9, 12):
self.data.costs_2015.s_cost[12] += self.data.costs_2015.s_cost[j]
def calc_tf_coil_costs(self):
"""Function to calculate the cost of the TF coils for the power plant
This routine calculates the cost of the TF coils for a fusion power
plant based on the costings in the PROCESS costs Paper.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(13, 20):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_tf_coils
# TF coil insertion and welding costs ($)
self.data.costs_2015.s_label[13] = "TF Coil insertion and welding"
# ITER coil insertion and welding cost (2014 $)
self.data.costs_2015.s_cref[13] = 258.0e6
# Scale with total TF coil length (m)
self.data.costs_2015.s_k[13] = (
self.data.tfcoil.n_tf_coils * self.data.tfcoil.len_tf_coil
)
self.data.costs_2015.s_kref[13] = 18.0e0 * 34.1e0
self.data.costs_2015.s_cost[13] = (
self.data.costs_2015.s_cost_factor[13]
* self.data.costs_2015.s_cref[13]
* (self.data.costs_2015.s_k[13] / self.data.costs_2015.s_kref[13])
** self.data.costs.costexp
)
# TF coil winding costs ($)
self.data.costs_2015.s_label[15] = "TF coil winding"
# ITER winding cost (2014 $)
self.data.costs_2015.s_cref[15] = 414.0e6
# Scale with the total turn length (m)
self.data.costs_2015.s_k[15] = (
self.data.tfcoil.n_tf_coils
* self.data.tfcoil.len_tf_coil
* self.data.tfcoil.n_tf_coil_turns
)
self.data.costs_2015.s_kref[15] = 82249.0e0
self.data.costs_2015.s_cost[15] = (
self.data.costs_2015.s_cost_factor[15]
* self.data.costs_2015.s_cref[15]
* (self.data.costs_2015.s_k[15] / self.data.costs_2015.s_kref[15])
** self.data.costs.costexp
)
# Copper stand cost for TF coil ($)
self.data.costs_2015.s_label[16] = "Copper strand for TF coil"
# ITER Chromium plated Cu strand for TF SC cost (2014 $)
self.data.costs_2015.s_cref[16] = 21.0e6
# Scale with total copper mass (kg)
self.data.costs_2015.s_k[16] = (
self.data.tfcoil.m_tf_coil_copper * self.data.tfcoil.n_tf_coils
)
self.data.costs_2015.s_kref[16] = 244.0e3
self.data.costs_2015.s_cost[16] = (
self.data.costs_2015.s_cost_factor[16]
* self.data.costs_2015.s_cref[16]
* (self.data.costs_2015.s_k[16] / self.data.costs_2015.s_kref[16])
** self.data.costs.costexp
)
# superconductor strand cost ($)
self.data.costs_2015.s_label[17] = (
"Strands with Nb3Sn superconductor and copper stabiliser"
)
# ITER Nb3Sn SC strands cost (2014 $)
self.data.costs_2015.s_cref[17] = 526.0e6
# Scale with the total mass of Nb3Sn (kg)
self.data.costs_2015.s_k[17] = (
self.data.tfcoil.m_tf_coil_superconductor * self.data.tfcoil.n_tf_coils
)
self.data.costs_2015.s_kref[17] = 210.0e3
self.data.costs_2015.s_cost[17] = (
self.data.costs_2015.s_cost_factor[17]
* self.data.costs_2015.s_cref[17]
* (self.data.costs_2015.s_k[17] / self.data.costs_2015.s_kref[17])
** self.data.costs.costexp
)
# Superconductor testing cost ($)
self.data.costs_2015.s_label[18] = "Testing of superconducting strands"
# ITER Nb3Sn strand test costs (2014 $)
self.data.costs_2015.s_cref[18] = 4.0e6
self.data.costs_2015.s_cost[18] = (
self.data.costs_2015.s_cost_factor[18] * self.data.costs_2015.s_cref[18]
)
# Superconductor cabling and jacketing cost ($)
self.data.costs_2015.s_label[19] = "Cabling and jacketing"
# ITER cabling and jacketing costs (2014 $)
self.data.costs_2015.s_cref[19] = 81.0e6
# Scale with total turn length.
self.data.costs_2015.s_k[19] = (
self.data.tfcoil.n_tf_coils
* self.data.tfcoil.len_tf_coil
* self.data.tfcoil.n_tf_coil_turns
)
self.data.costs_2015.s_kref[19] = 82249.0e0
self.data.costs_2015.s_cost[19] = (
self.data.costs_2015.s_cost_factor[19]
* self.data.costs_2015.s_cref[19]
* (self.data.costs_2015.s_k[19] / self.data.costs_2015.s_kref[19])
** self.data.costs.costexp
)
# Total TF coil costs ($)
self.data.costs_2015.s_label[20] = "Total TF coil costs"
self.data.costs_2015.s_cost[20] = 0.0e0
for j in range(13, 20):
self.data.costs_2015.s_cost[20] += self.data.costs_2015.s_cost[j]
def calc_remote_handling_costs(self):
"""Function to calculate the cost of the remote handling facilities
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(27, 31):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_rh
# K:\Power Plant Physics and Technology\Costs\Remote handling
# From Sam Ha.
self.data.costs_2015.s_label[27] = "Moveable equipment"
self.data.costs_2015.s_cref[27] = 1.0e6 * (
139.0e0 * self.data.costs.num_rh_systems + 410.0e0
)
# Scale with total mass of armour, first wall and blanket (kg)
self.data.costs_2015.s_kref[27] = 4.35e6
self.data.costs_2015.s_k[27] = self.data.fwbs.armour_fw_bl_mass
self.data.costs_2015.s_cost[27] = (
self.data.costs_2015.s_cost_factor[27]
* self.data.costs_2015.s_cref[27]
* (self.data.costs_2015.s_k[27] / self.data.costs_2015.s_kref[27])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[28] = (
"Active maintenance facility with fixed equipment"
)
self.data.costs_2015.s_cref[28] = 1.0e6 * (
95.0e0 * self.data.costs.num_rh_systems + 2562.0e0
)
# Scale with total mass of armour, first wall and blanket (kg)
self.data.costs_2015.s_kref[28] = 4.35e6
self.data.costs_2015.s_k[28] = self.data.fwbs.armour_fw_bl_mass
self.data.costs_2015.s_cost[28] = (
self.data.costs_2015.s_cost_factor[28]
* self.data.costs_2015.s_cref[28]
* (self.data.costs_2015.s_k[28] / self.data.costs_2015.s_kref[28])
** self.data.costs.costexp
)
# s(30) is not in use
self.data.costs_2015.s_label[30] = "Total remote handling costs"
self.data.costs_2015.s_cost[30] = (
self.data.costs_2015.s_cost[27] + self.data.costs_2015.s_cost[28]
)
def calc_n_plant_and_vv_costs(self):
"""Function to calculate the cost of the nitrogen plant and vacuum vessel
This routine calculates the cost of the nitrogen plant and vacuum vessel
for a fusion power plant based on the costings in the PROCESS costs paper.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(31, 34):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_vv
# Vacuum vessel
self.data.costs_2015.s_label[31] = "Vacuum vessel"
# ITER reference vacuum vessel cost (2014 $)
self.data.costs_2015.s_cref[31] = 537.0e6
# Scale with outermost midplane radius of vacuum vessel squared (m2)
self.data.costs_2015.s_k[31] = (
self.data.build.r_shld_outboard_outer + self.data.build.dr_vv_outboard
) ** 2
self.data.costs_2015.s_kref[31] = 94.09e0
self.data.costs_2015.s_cost[31] = (
self.data.costs_2015.s_cost_factor[31]
* self.data.costs_2015.s_cref[31]
* (self.data.costs_2015.s_k[31] / self.data.costs_2015.s_kref[31])
** self.data.costs.costexp
)
# Nitrogen plant
self.data.costs_2015.s_label[32] = "Liquid nitrogen plant"
# ITER reference cost (2014 $)
self.data.costs_2015.s_cref[32] = 86.0e6
# Scale with 4.5K cryopower (W)
self.data.costs_2015.s_k[32] = self.data.heat_transport.helpow
self.data.costs_2015.s_kref[32] = 50.0e3
self.data.costs_2015.s_cost[32] = (
self.data.costs_2015.s_cost_factor[32]
* self.data.costs_2015.s_cref[32]
* (self.data.costs_2015.s_k[32] / self.data.costs_2015.s_kref[32])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[33] = (
"Total liquid nitrogen plant and vacuum vessel"
)
self.data.costs_2015.s_cost[33] = 0.0e0
for j in range(31, 33):
self.data.costs_2015.s_cost[33] += self.data.costs_2015.s_cost[j]
def calc_energy_conversion_system(self):
"""Function to calculate the cost of the energy conversion system
This routine calculates the cost of the energy conversion system
for a fusion power plant based on the costings in the PROCESS costs paper.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
self.data.costs_2015.s_label[34] = "Energy conversion system"
# Set cost factor for energy conversion system
self.data.costs_2015.s_cost_factor[34] = self.data.costs.cost_factor_bop
# Cost of reference energy conversion system (Rolls Royce)
self.data.costs_2015.s_cref[34] = 511.0e6
# Scale with gross electric power (MWe)
self.data.costs_2015.s_k[34] = self.data.heat_transport.p_plant_electric_gross_mw
self.data.costs_2015.s_kref[34] = 692.0e0
self.data.costs_2015.s_cost[34] = (
self.data.costs_2015.s_cost_factor[34]
* self.data.costs_2015.s_cref[34]
* (self.data.costs_2015.s_k[34] / self.data.costs_2015.s_kref[34])
** self.data.costs.costexp
)
def calc_remaining_subsystems(self):
"""Function to calculate the cost of the remaining subsystems
This routine calculates the cost of the remaining subsystems
for a fusion power plant based on the costings in the PROCESS costs paper.
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
for i in range(35, 60):
self.data.costs_2015.s_cost_factor[i] = self.data.costs.cost_factor_misc
self.data.costs_2015.s_label[35] = "CS and PF coils"
# # Cost of ITER CS and PF magnets
self.data.costs_2015.s_cref[35] = 1538.0e6
# Scale with sum of (A x turns x radius) of CS and all PF coils
self.data.costs_2015.s_k[35] = self.data.pf_coil.itr_sum
self.data.costs_2015.s_kref[35] = 7.4e8
self.data.costs_2015.s_cost[35] = (
self.data.costs_2015.s_cost_factor[35]
* self.data.costs_2015.s_cref[35]
* (self.data.costs_2015.s_k[35] / self.data.costs_2015.s_kref[35])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[36] = (
"Vacuum vessel in-wall shielding, ports and in-vessel coils"
)
# Cost of ITER VV in-wall shielding, ports and in-vessel coils
self.data.costs_2015.s_cref[36] = 211.0e6
# Scale with vacuum vessel mass (kg)
self.data.costs_2015.s_k[36] = self.data.fwbs.m_vv
self.data.costs_2015.s_kref[36] = 5.2360e6
self.data.costs_2015.s_cost[36] = (
self.data.costs_2015.s_cost_factor[36]
* self.data.costs_2015.s_cref[36]
* (self.data.costs_2015.s_k[36] / self.data.costs_2015.s_kref[36])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[37] = "Divertor"
# Cost of ITER divertor
self.data.costs_2015.s_cref[37] = 381.0e6
# Scale with max power to SOL (MW)
self.data.costs_2015.s_k[37] = self.data.physics.p_plasma_separatrix_mw
self.data.costs_2015.s_kref[37] = 140.0e0
self.data.costs_2015.s_cost[37] = (
self.data.costs_2015.s_cost_factor[37]
* self.data.costs_2015.s_cref[37]
* (self.data.costs_2015.s_k[37] / self.data.costs_2015.s_kref[37])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[38] = "not used"
self.data.costs_2015.s_label[39] = "not used"
self.data.costs_2015.s_label[40] = (
"Ex-vessel neutral beam remote handling equipment"
)
# Cost of ITER Ex-vessel NBI RH equipment
# Increased to 90 Mdollar because of press release
self.data.costs_2015.s_cref[40] = 90.0e6
# Scale with total aux injected power (MW)
self.data.costs_2015.s_k[40] = self.data.current_drive.p_hcd_injected_total_mw
self.data.costs_2015.s_kref[40] = 50.0e0
self.data.costs_2015.s_cost[40] = (
self.data.costs_2015.s_cost_factor[40]
* self.data.costs_2015.s_cref[40]
* (self.data.costs_2015.s_k[40] / self.data.costs_2015.s_kref[40])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[41] = "not used"
self.data.costs_2015.s_label[42] = "Vacuum vessel pressure suppression system"
# Cost of ITER Vacuum vessel pressure suppression system
self.data.costs_2015.s_cref[42] = 40.0e6
# Scale with total thermal power removed from fusion core (MW)
self.data.costs_2015.s_k[42] = (
self.data.heat_transport.p_plant_primary_heat_mw
+ self.data.heat_transport.p_plant_secondary_heat_mw
)
self.data.costs_2015.s_kref[42] = 550.0e0
self.data.costs_2015.s_cost[42] = (
self.data.costs_2015.s_cost_factor[42]
* self.data.costs_2015.s_cref[42]
* (self.data.costs_2015.s_k[42] / self.data.costs_2015.s_kref[42])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[43] = "Cryostat"
# Cost of ITER cryostat
self.data.costs_2015.s_cref[43] = 351.0e6
# Scale with cryostat external volume (m3)
self.data.costs_2015.s_k[43] = (
(np.pi * self.data.fwbs.r_cryostat_inboard**2.0e0)
* 2.0e0
* self.data.fwbs.z_cryostat_half_inside
)
self.data.costs_2015.s_kref[43] = 18700.0e0
self.data.costs_2015.s_cost[43] = (
self.data.costs_2015.s_cost_factor[43]
* self.data.costs_2015.s_cref[43]
* (self.data.costs_2015.s_k[43] / self.data.costs_2015.s_kref[43])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[44] = "Heat removal system"
# Cost of ITER cooling water system
self.data.costs_2015.s_cref[44] = 724.0e6
# Scale with total thermal power removed from fusion core (MW)
self.data.costs_2015.s_k[44] = (
self.data.heat_transport.p_plant_primary_heat_mw
+ self.data.heat_transport.p_plant_secondary_heat_mw
)
self.data.costs_2015.s_kref[44] = 550.0e0
self.data.costs_2015.s_cost[44] = (
self.data.costs_2015.s_cost_factor[44]
* self.data.costs_2015.s_cref[44]
* (self.data.costs_2015.s_k[44] / self.data.costs_2015.s_kref[44])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[45] = "Thermal shields"
# Cost of ITER thermal shields
self.data.costs_2015.s_cref[45] = 126.0e6
# Scale with cryostat surface area (m2)
self.data.costs_2015.s_k[45] = (
2.0e0
* np.pi
* self.data.fwbs.r_cryostat_inboard
* 2.0e0
* self.data.fwbs.z_cryostat_half_inside
+ 2 * (np.pi * self.data.fwbs.r_cryostat_inboard**2)
)
self.data.costs_2015.s_kref[45] = 3902.0e0
self.data.costs_2015.s_cost[45] = (
self.data.costs_2015.s_cost_factor[45]
* self.data.costs_2015.s_cref[45]
* (self.data.costs_2015.s_k[45] / self.data.costs_2015.s_kref[45])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[46] = "Pellet injection system"
# Cost of ITER pellet injector and pellet injection system
self.data.costs_2015.s_cref[46] = 25.0e6
# Scale with fusion power (MW)
self.data.costs_2015.s_k[46] = self.data.physics.p_fusion_total_mw
self.data.costs_2015.s_kref[46] = 500.0e0
self.data.costs_2015.s_cost[46] = (
self.data.costs_2015.s_cost_factor[46]
* self.data.costs_2015.s_cref[46]
* (self.data.costs_2015.s_k[46] / self.data.costs_2015.s_kref[46])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[47] = "Gas injection and wall conditioning system"
# # Cost of ITER gas injection system, GDC, Gi valve boxes
self.data.costs_2015.s_cref[47] = 32.0e6
# Scale with fusion power (MW)
self.data.costs_2015.s_k[47] = self.data.physics.p_fusion_total_mw
self.data.costs_2015.s_kref[47] = 500.0e0
self.data.costs_2015.s_cost[47] = (
self.data.costs_2015.s_cost_factor[47]
* self.data.costs_2015.s_cref[47]
* (self.data.costs_2015.s_k[47] / self.data.costs_2015.s_kref[47])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[48] = "Vacuum pumping"
# Cost of ITER vacuum pumping
self.data.costs_2015.s_cref[48] = 201.0e6
# Scale with fusion power (MW)
self.data.costs_2015.s_k[48] = self.data.physics.p_fusion_total_mw
self.data.costs_2015.s_kref[48] = 500.0e0
self.data.costs_2015.s_cost[48] = (
self.data.costs_2015.s_cost_factor[48]
* self.data.costs_2015.s_cref[48]
* (self.data.costs_2015.s_k[48] / self.data.costs_2015.s_kref[48])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[49] = "Tritium plant"
# Cost of ITER tritium plant
self.data.costs_2015.s_cref[49] = 226.0e6
# Scale with fusion power (MW)
self.data.costs_2015.s_k[49] = self.data.physics.p_fusion_total_mw
self.data.costs_2015.s_kref[49] = 500.0e0
self.data.costs_2015.s_cost[49] = (
self.data.costs_2015.s_cost_factor[49]
* self.data.costs_2015.s_cref[49]
* (self.data.costs_2015.s_k[49] / self.data.costs_2015.s_kref[49])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[50] = "Cryoplant and distribution"
# Cost of ITER Cryoplant and distribution
self.data.costs_2015.s_cref[50] = 397.0e6
# Scale with heat removal at 4.5 K approx (W)
self.data.costs_2015.s_k[50] = self.data.heat_transport.helpow
self.data.costs_2015.s_kref[50] = 50000.0e0
self.data.costs_2015.s_cost[50] = (
self.data.costs_2015.s_cost_factor[50]
* self.data.costs_2015.s_cref[50]
* (self.data.costs_2015.s_k[50] / self.data.costs_2015.s_kref[50])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[51] = "Electrical power supply and distribution"
# Cost of ITER electrical power supply and distribution
self.data.costs_2015.s_cref[51] = 1188.0e6
# Scale with total magnetic energy in the
# poloidal field / resistive diffusion time (W)
# For ITER value see
# K:\Power Plant Physics and Technology\PROCESS\
# PROCESS documentation papers\resistive diffusion time.xmcd or pdf
self.data.costs_2015.s_k[51] = (
self.data.pf_power.ensxpfm * 1.0e6 / self.data.physics.t_plasma_res_diffusion
)
self.data.costs_2015.s_kref[51] = 8.0e9 / 953.0e0
self.data.costs_2015.s_cost[51] = (
self.data.costs_2015.s_cost_factor[51]
* self.data.costs_2015.s_cref[51]
* (self.data.costs_2015.s_k[51] / self.data.costs_2015.s_kref[51])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[52] = (
"Neutral beam heating and current drive system"
)
# Cost of ITER NB H and CD
self.data.costs_2015.s_cref[52] = 814.0e6
# Scale with total auxiliary injected power (MW)
self.data.costs_2015.s_k[52] = self.data.current_drive.p_hcd_injected_total_mw
self.data.costs_2015.s_kref[52] = 50.0e0
self.data.costs_2015.s_cost[52] = (
self.data.costs_2015.s_cost_factor[52]
* self.data.costs_2015.s_cref[52]
* (self.data.costs_2015.s_k[52] / self.data.costs_2015.s_kref[52])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[53] = "Diagnostics systems"
# Cost of ITER diagnostic systems
self.data.costs_2015.s_cref[53] = 640.0e6
# No scaling
self.data.costs_2015.s_cost[53] = (
self.data.costs_2015.s_cost_factor[53] * self.data.costs_2015.s_cref[53]
)
self.data.costs_2015.s_label[54] = "Radiological protection"
# Cost of ITER radiological protection
self.data.costs_2015.s_cref[54] = 19.0e6
# Scale with fusion power (MW)
self.data.costs_2015.s_k[54] = self.data.physics.p_fusion_total_mw
self.data.costs_2015.s_kref[54] = 500.0e0
self.data.costs_2015.s_cost[54] = (
self.data.costs_2015.s_cost_factor[54]
* self.data.costs_2015.s_cref[54]
* (self.data.costs_2015.s_k[54] / self.data.costs_2015.s_kref[54])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[55] = "Access control and security systems"
# Cost of ITER access control and security systems
# Scale with area of cryostat (m2)
self.data.costs_2015.s_k[55] = np.pi * self.data.fwbs.r_cryostat_inboard**2
self.data.costs_2015.s_kref[55] = 640.0e0
self.data.costs_2015.s_cref[55] = 42.0e6
self.data.costs_2015.s_cost[55] = (
self.data.costs_2015.s_cost_factor[55]
* self.data.costs_2015.s_cref[55]
* (self.data.costs_2015.s_k[55] / self.data.costs_2015.s_kref[55])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[56] = "Assembly"
# Cost of ITER assembly
self.data.costs_2015.s_cref[56] = 732.0e6
# Scale with total cost of reactor items (cryostat and everything inside it)
self.data.costs_2015.s_k[56] = (
self.data.costs_2015.s_cost[20]
+ self.data.costs_2015.s_cost[26]
+ self.data.costs_2015.s_cost[31]
+ self.data.costs_2015.s_cost[35]
+ self.data.costs_2015.s_cost[36]
+ self.data.costs_2015.s_cost[37]
+ self.data.costs_2015.s_cost[43]
+ self.data.costs_2015.s_cost[45]
+ self.data.costs_2015.s_cost[48]
)
self.data.costs_2015.s_kref[56] = (
self.data.costs_2015.s_cref[20]
+ self.data.costs_2015.s_cref[26]
+ self.data.costs_2015.s_cref[31]
+ self.data.costs_2015.s_cref[35]
+ self.data.costs_2015.s_cref[36]
+ self.data.costs_2015.s_cref[37]
+ self.data.costs_2015.s_cref[43]
+ self.data.costs_2015.s_cref[45]
+ self.data.costs_2015.s_cref[48]
)
self.data.costs_2015.s_cost[56] = (
self.data.costs_2015.s_cost_factor[56]
* self.data.costs_2015.s_cref[56]
* (self.data.costs_2015.s_k[56] / self.data.costs_2015.s_kref[56])
)
self.data.costs_2015.s_label[57] = "Control and communication"
# Cost of ITER control and data access and communication
self.data.costs_2015.s_cref[57] = 219.0e6
# Scale with total cost of reactor items (cryostat and everythign inside it)
self.data.costs_2015.s_k[57] = (
self.data.costs_2015.s_cost[20]
+ self.data.costs_2015.s_cost[26]
+ self.data.costs_2015.s_cost[31]
+ self.data.costs_2015.s_cost[35]
+ self.data.costs_2015.s_cost[36]
+ self.data.costs_2015.s_cost[37]
+ self.data.costs_2015.s_cost[43]
+ self.data.costs_2015.s_cost[45]
+ self.data.costs_2015.s_cost[48]
)
self.data.costs_2015.s_kref[57] = (
self.data.costs_2015.s_cref[20]
+ self.data.costs_2015.s_cref[26]
+ self.data.costs_2015.s_cref[31]
+ self.data.costs_2015.s_cref[35]
+ self.data.costs_2015.s_cref[36]
+ self.data.costs_2015.s_cref[37]
+ self.data.costs_2015.s_cref[43]
+ self.data.costs_2015.s_cref[45]
+ self.data.costs_2015.s_cref[48]
)
self.data.costs_2015.s_cost[57] = (
self.data.costs_2015.s_cost_factor[57]
* self.data.costs_2015.s_cref[57]
* (self.data.costs_2015.s_k[57] / self.data.costs_2015.s_kref[57])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[58] = "Additional project expenditure"
# Cost of ITER additional ITER IO expenditure
self.data.costs_2015.s_cref[58] = 1624.0e6
self.data.costs_2015.s_cost[58] = (
self.data.costs_2015.s_cost_factor[58] * self.data.costs_2015.s_cref[58]
)
# Calculate miscellaneous costs
self.data.costs_2015.s_label[59] = "Logistics"
self.data.costs_2015.s_cref[59] = 129.0e6
# Scale with cryostat external volume (m)
self.data.costs_2015.s_k[59] = (
np.pi
* self.data.fwbs.r_cryostat_inboard**2
* 2.0e0
* self.data.fwbs.z_cryostat_half_inside
)
self.data.costs_2015.s_kref[59] = 18700.0e0
self.data.costs_2015.s_cost[59] = (
self.data.costs_2015.s_cost_factor[59]
* self.data.costs_2015.s_cref[59]
* (self.data.costs_2015.s_k[59] / self.data.costs_2015.s_kref[59])
** self.data.costs.costexp
)
self.data.costs_2015.s_label[60] = "Total remaining subsystem costs"
self.data.costs_2015.s_cost[60] = 0.0e0
for j in range(35, 60):
self.data.costs_2015.s_cost[60] += self.data.costs_2015.s_cost[j]
@staticmethod
def value_function(x):
"""Value function
Function for separative work unit calculation for enrichment cost
PROCESS Costs Paper (M. Kovari, J. Morris)
"""
return (1.0e0 - 2.0e0 * x) * np.log((1.0e0 - x) / x)
@staticmethod
def ocost(file, descr, vname, value):
"""Routine to print out the code, description and value
of a cost item from array s in costs_2015
"""
if descr == "not used":
return
po.ovarre(file, descr, str(vname), value)
```
|