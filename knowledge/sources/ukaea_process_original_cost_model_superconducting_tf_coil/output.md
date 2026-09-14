---
source: "https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs/"
source_type: "url"
extracted_at: "2026-09-14T04:25:19.316850+00:00"
content_hash_sha256: "9f6fd08bdd66259fdfa9aeb7109a79f2db1f04f3725063291ef22748710502c8"
backend: "trafilatura"
title: "costs"
---

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
1227
1228
1229
1230
1231
1232
1233
1234
1235
1236
1237
1238
1239
1240
1241
1242
1243
1244
1245
1246
1247
1248
1249
1250
1251
1252
1253
1254
1255
1256
1257
1258
1259
1260
1261
1262
1263
1264
1265
1266
1267
1268
1269
1270
1271
1272
1273
1274
1275
1276
1277
1278
1279
1280
1281
1282
1283
1284
1285
1286
1287
1288
1289
1290
1291
1292
1293
1294
1295
1296
1297
1298
1299
1300
1301
1302
1303
1304
1305
1306
1307
1308
1309
1310
1311
1312
1313
1314
1315
1316
1317
1318
1319
1320
1321
1322
1323
1324
1325
1326
1327
1328
1329
1330
1331
1332
1333
1334
1335
1336
1337
1338
1339
1340
1341
1342
1343
1344
1345
1346
1347
1348
1349
1350
1351
1352
1353
1354
1355
1356
1357
1358
1359
1360
1361
1362
1363
1364
1365
1366
1367
1368
1369
1370
1371
1372
1373
1374
1375
1376
1377
1378
1379
1380
1381
1382
1383
1384
1385
1386
1387
1388
1389
1390
1391
1392
1393
1394
1395
1396
1397
1398
1399
1400
1401
1402
1403
1404
1405
1406
1407
1408
1409
1410
1411
1412
1413
1414
1415
1416
1417
1418
1419
1420
1421
1422
1423
1424
1425
1426
1427
1428
1429
1430
1431
1432
1433
1434
1435
1436
1437
1438
1439
1440
1441
1442
1443
1444
1445
1446
1447
1448
1449
1450
1451
1452
1453
1454
1455
1456
1457
1458
1459
1460
1461
1462
1463
1464
1465
1466
1467
1468
1469
1470
1471
1472
1473
1474
1475
1476
1477
1478
1479
1480
1481
1482
1483
1484
1485
1486
1487
1488
1489
1490
1491
1492
1493
1494
1495
1496
1497
1498
1499
1500
1501
1502
1503
1504
1505
1506
1507
1508
1509
1510
1511
1512
1513
1514
1515
1516
1517
1518
1519
1520
1521
1522
1523
1524
1525
1526
1527
1528
1529
1530
1531
1532
1533
1534
1535
1536
1537
1538
1539
1540
1541
1542
1543
1544
1545
1546
1547
1548
1549
1550
1551
1552
1553
1554
1555
1556
1557
1558
1559
1560
1561
1562
1563
1564
1565
1566
1567
1568
1569
1570
1571
1572
1573
1574
1575
1576
1577
1578
1579
1580
1581
1582
1583
1584
1585
1586
1587
1588
1589
1590
1591
1592
1593
1594
1595
1596
1597
1598
1599
1600
1601
1602
1603
1604
1605
1606
1607
1608
1609
1610
1611
1612
1613
1614
1615
1616
1617
1618
1619
1620
1621
1622
1623
1624
1625
1626
1627
1628
1629
1630
1631
1632
1633
1634
1635
1636
1637
1638
1639
1640
1641
1642
1643
1644
1645
1646
1647
1648
1649
1650
1651
1652
1653
1654
1655
1656
1657
1658
1659
1660
1661
1662
1663
1664
1665
1666
1667
1668
1669
1670
1671
1672
1673
1674
1675
1676
1677
1678
1679
1680
1681
1682
1683
1684
1685
1686
1687
1688
1689
1690
1691
1692
1693
1694
1695
1696
1697
1698
1699
1700
1701
1702
1703
1704
1705
1706
1707
1708
1709
1710
1711
1712
1713
1714
1715
1716
1717
1718
1719
1720
1721
1722
1723
1724
1725
1726
1727
1728
1729
1730
1731
1732
1733
1734
1735
1736
1737
1738
1739
1740
1741
1742
1743
1744
1745
1746
1747
1748
1749
1750
1751
1752
1753
1754
1755
1756
1757
1758
1759
1760
1761
1762
1763
1764
1765
1766
1767
1768
1769
1770
1771
1772
1773
1774
1775
1776
1777
1778
1779
1780
1781
1782
1783
1784
1785
1786
1787
1788
1789
1790
1791
1792
1793
1794
1795
1796
1797
1798
1799
1800
1801
1802
1803
1804
1805
1806
1807
1808
1809
1810
1811
1812
1813
1814
1815
1816
1817
1818
1819
1820
1821
1822
1823
1824
1825
1826
1827
1828
1829
1830
1831
1832
1833
1834
1835
1836
1837
1838
1839
1840
1841
1842
1843
1844
1845
1846
1847
1848
1849
1850
1851
1852
1853
1854
1855
1856
1857
1858
1859
1860
1861
1862
1863
1864
1865
1866
1867
1868
1869
1870
1871
1872
1873
1874
1875
1876
1877
1878
1879
1880
1881
1882
1883
1884
1885
1886
1887
1888
1889
1890
1891
1892
1893
1894
1895
1896
1897
1898
1899
1900
1901
1902
1903
1904
1905
1906
1907
1908
1909
1910
1911
1912
1913
1914
1915
1916
1917
1918
1919
1920
1921
1922
1923
1924
1925
1926
1927
1928
1929
1930
1931
1932
1933
1934
1935
1936
1937
1938
1939
1940
1941
1942
1943
1944
1945
1946
1947
1948
1949
1950
1951
1952
1953
1954
1955
1956
1957
1958
1959
1960
1961
1962
1963
1964
1965
1966
1967
1968
1969
1970
1971
1972
1973
1974
1975
1976
1977
1978
1979
1980
1981
1982
1983
1984
1985
1986
1987
1988
1989
1990
1991
1992
1993
1994
1995
1996
1997
1998
1999
2000
2001
2002
2003
2004
2005
2006
2007
2008
2009
2010
2011
2012
2013
2014
2015
2016
2017
2018
2019
2020
2021
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2032
2033
2034
2035
2036
2037
2038
2039
2040
2041
2042
2043
2044
2045
2046
2047
2048
2049
2050
2051
2052
2053
2054
2055
2056
2057
2058
2059
2060
2061
2062
2063
2064
2065
2066
2067
2068
2069
2070
2071
2072
2073
2074
2075
2076
2077
2078
2079
2080
2081
2082
2083
2084
2085
2086
2087
2088
2089
2090
2091
2092
2093
2094
2095
2096
2097
2098
2099
2100
2101
2102
2103
2104
2105
2106
2107
2108
2109
2110
2111
2112
2113
2114
2115
2116
2117
2118
2119
2120
2121
2122
2123
2124
2125
2126
2127
2128
2129
2130
2131
2132
2133
2134
2135
2136
2137
2138
2139
2140
2141
2142
2143
2144
2145
2146
2147
2148
2149
2150
2151
2152
2153
2154
2155
2156
2157
2158
2159
2160
2161
2162
2163
2164
2165
2166
2167
2168
2169
2170
2171
2172
2173
2174
2175
2176
2177
2178
2179
2180
2181
2182
2183
2184
2185
2186
2187
2188
2189
2190
2191
2192
2193
2194
2195
2196
2197
2198
2199
2200
2201
2202
2203
2204
2205
2206
2207
2208
2209
2210
2211
2212
2213
2214
2215
2216
2217
2218
2219
2220
2221
2222
2223
2224
2225
2226
2227
2228
2229
2230
2231
2232
2233
2234
2235
2236
2237
2238
2239
2240
2241
2242
2243
2244
2245
2246
2247
2248
2249
2250
2251
2252
2253
2254
2255
2256
2257
2258
2259
2260
2261
2262
2263
2264
2265
2266
2267
2268
2269
2270
2271
2272
2273
2274
2275
2276
2277
2278
2279
2280
2281
2282
2283
2284
2285
2286
2287
2288
2289
2290
2291
2292
2293
2294
2295
2296
2297
2298
2299
2300
2301
2302
2303
2304
2305
2306
2307
2308
2309
2310
2311
2312
2313
2314
2315
2316
2317
2318
2319
2320
2321
2322
2323
2324
2325
2326
2327
2328
2329
2330
2331
2332
2333
2334
2335
2336
2337
2338
2339
2340
2341
2342
2343
2344
2345
2346
2347
2348
2349
2350
2351
2352
2353
2354
2355
2356
2357
2358
2359
2360
2361
2362
2363
2364
2365
2366
2367
2368
2369
2370
2371
2372
2373
2374
2375
2376
2377
2378
2379
2380
2381
2382
2383
2384
2385
2386
2387
2388
2389
2390
2391
2392
2393
2394
2395
2396
2397
2398
2399
2400
2401
2402
2403
2404
2405
2406
2407
2408
2409
2410
2411
2412
2413
2414
2415
2416
2417
2418
2419
2420
2421
2422
2423
2424
2425
2426
2427
2428
2429
2430
2431
2432
2433
2434
2435
2436
2437
2438
2439
2440
2441
2442
2443
2444
2445
2446
2447
2448
2449
2450
2451
2452
2453
2454
2455
2456
2457
2458
2459
2460
2461
2462
2463
2464
2465
2466
2467
2468
2469
2470
2471
2472
2473
2474
2475
2476
2477
2478
2479
2480
2481
2482
2483
2484
2485
2486
2487
2488
2489
2490
2491
2492
2493
2494
2495
2496
2497
2498
2499
2500
2501
2502
2503
2504
2505
2506
2507
2508
2509
2510
2511
2512
2513
2514
2515
2516
2517
2518
2519
2520
2521
2522
2523
2524
2525
2526
2527
2528
2529
2530
2531
2532
2533
2534
2535
2536
2537
2538
2539
2540
2541
2542
2543
2544
2545
2546
2547
2548
2549
2550
2551
2552
2553
2554
2555
2556
2557
2558
2559
2560
2561
2562
2563
2564
2565
2566
2567
2568
2569
2570
2571
2572
2573
2574
2575
2576
2577
2578
2579
2580
2581
2582
2583
2584
2585
2586
2587
2588
2589
2590
2591
2592
2593
2594
2595
2596
2597
2598
2599
2600
2601
2602
2603
2604
2605
2606
2607
2608
2609
2610
2611
2612
2613
2614
2615
2616
2617
2618
2619
2620
2621
2622
2623
2624
2625
2626
2627
2628
2629
2630
2631
2632
2633
2634
2635
2636
2637
2638
2639
2640
2641
2642
2643
2644
2645
2646
2647
2648
2649
2650
2651
2652
2653
2654
2655
2656
2657
2658
2659
2660
2661
2662
2663
2664
2665
2666
2667
2668
2669
2670
2671
2672
2673
2674
2675
2676
2677
2678
2679
2680
2681
2682
2683
2684
2685
2686
2687
2688
2689
2690
2691
2692
2693
2694
2695
2696
2697
2698
2699
2700
2701
2702
2703
2704
2705
2706
2707
2708
2709
2710
2711
2712
2713
2714
2715
2716
2717
2718
2719
2720
2721
2722
2723
2724
2725
2726
2727
2728
2729
2730
2731
2732
2733
2734
2735
2736
2737
2738
2739
2740
2741
2742
2743
2744
2745
2746
2747
2748
2749
2750
2751
2752
2753
2754
2755
2756
2757
2758
2759
2760
2761
2762
2763
2764
2765
2766
2767
2768
2769
2770
2771
2772
2773
2774
2775
2776
2777
2778
2779
2780
2781
2782
2783
2784
2785
2786
2787
2788
2789
2790
2791
2792
2793
2794
2795
2796
2797
2798
2799
2800
2801
2802
2803
2804
2805
2806
2807
2808
2809
2810
2811
2812
2813
2814
2815
2816
2817
2818
2819
2820
2821
2822
2823
2824
2825
2826
2827
2828
2829
2830
2831
2832
2833
2834
2835
2836
2837
2838
2839
2840
2841
2842
2843
2844
2845
2846
2847
2848
2849
2850
2851
2852
2853
2854
2855
2856
2857
2858
2859
2860
2861
2862
2863
2864
2865
2866
2867
2868
2869
2870
2871
2872
2873
2874
2875
2876
2877
2878
2879
2880
2881
2882
2883
2884
2885
2886
2887
2888
2889
2890
2891
2892
2893
2894
2895
2896
2897
2898
2899
2900
2901
2902
2903
2904
2905
2906
2907
2908
2909
2910
2911
2912
2913
2914
2915
2916
2917
2918
2919
2920
2921
2922
2923
2924
2925
2926
2927
2928
2929
2930
2931
2932
2933
2934
2935
2936
2937
2938
2939
2940
2941
2942
2943
2944
2945
2946
2947
2948
2949
2950
2951
2952
2953
2954
2955
2956
2957
2958
2959
2960
2961
2962
2963
2964
2965
2966
2967
2968
2969
2970
2971
2972
2973
2974
2975
2976
2977
2978
2979
2980
2981
2982
2983
2984
2985
2986
2987
2988
2989
2990
2991
2992
2993
2994
2995
2996
2997
2998
2999
3000
3001
3002
3003
3004
3005
3006
3007
3008
3009
3010
3011
3012
3013
3014
3015
3016
3017
3018
3019
3020
3021
3022
3023
3024
3025
3026
3027 | ```
class Costs(Model):
"""Cost accounting calculations"""
def __init__(self):
self.outfile = constants.NOUT
def run(self):
"""Cost accounting for a fusion power plant
This routine performs the cost accounting for a fusion power plant.
The direct costs are calculated based on parameters input
from other sections of the code.
<P>Costs are in 1990 $, and assume first-of-a-kind components
unless otherwise stated. Account 22 costs include a multiplier
to account for Nth-of-a-kind cost reductions.
<P>The code is arranged in the order of the standard accounts.
"""
# Convert FPY component lifetimes to calendar years
# for replacement components
self.convert_fpy_to_calendar()
self.acc21()
# Account 22 : Fusion power island
self.acc22()
# Account 23 : Turbine plant equipment
self.acc23()
# Account 24 : Electric plant equipment
self.acc241() # Account 241 : Switchyard
self.acc242() # Account 242 : Transformers
self.acc243() # Account 243 : Low voltage
self.acc244() # Account 244 : Diesel generators
self.acc245() # Account 245 : Auxiliary facility power equipment
self.acc24() # Account 24 : Total
# Account 25 : Miscellaneous plant equipment
self.acc25()
# Account 26 : Heat rejection system
self.acc26()
# Total plant direct cost
# cdirt = c21 + c22 + self.data.costs.c23 + self.data.costs.c24 +
# self.data.costs.c25 + self.data.costs.c26
self.data.costs.cdirt = (
self.data.costs.c21
+ self.data.costs.c22
+ self.data.costs.c23
+ self.data.costs.c24
+ self.data.costs.c25
+ self.data.costs.c26
)
# Account 9 : Indirect cost and project contingency
self.acc9()
# Constructed cost
self.data.costs.concost = (
self.data.costs.cdirt + self.data.costs.cindrt + self.data.costs.ccont
)
# Cost of electricity
if (self.data.costs.ireactor == 1) and (self.data.costs.ipnet == 0):
self.coelc()
def output(self):
"""Output costs information"""
self.run()
if self.data.costs.output_costs == 0:
return
po.oheadr(self.outfile, "Power Reactor Costs (1990 US$)")
po.ovarre(
self.outfile,
"First wall / blanket life (years)",
"(life_blkt)",
self.data.fwbs.life_blkt,
)
if self.data.ife.ife != 1:
po.ovarre(
self.outfile,
"Divertor life (years)",
"(life_div)",
self.data.costs.life_div,
)
if self.data.physics.itart == 1:
po.ovarre(
self.outfile,
"Centrepost life (years)",
"(cplife_cal)",
self.data.costs.cplife_cal,
)
po.ovarre(
self.outfile, "Cost of electricity (m$/kWh)", "(coe)", self.data.costs.coe
)
po.osubhd(self.outfile, "Power Generation Costs :")
if self.data.costs.ifueltyp == 1:
po.oshead(self.outfile, "Replaceable Components Direct Capital Cost")
po.ovarre(
self.outfile,
"First wall direct capital cost (M$)",
"(fwallcst)",
self.data.costs.fwallcst,
)
po.ovarre(
self.outfile,
"Blanket direct capital cost (M$)",
"(blkcst)",
self.data.costs.blkcst,
)
if self.data.ife.ife != 1:
po.ovarre(
self.outfile,
"Divertor direct capital cost (M$)",
"(divcst)",
self.data.costs.divcst,
)
if self.data.physics.itart == 1:
po.ovarre(
self.outfile,
"Centrepost direct capital cost (M$)",
"(cpstcst)",
self.data.costs.cpstcst,
)
po.ovarre(
self.outfile,
"Plasma heating/CD system cap cost (M$)",
"",
self.data.costs.cdcost
* self.data.costs.fcdfuel
/ (1.0e0 - self.data.costs.fcdfuel),
)
po.ovarre(
self.outfile,
"Fraction of CD cost --> fuel cost",
"(fcdfuel)",
self.data.costs.fcdfuel,
)
else:
po.ovarre(
self.outfile,
"IFE driver system direct cap cost (M$)",
"",
self.data.costs.cdcost
* self.data.costs.fcdfuel
/ (1.0e0 - self.data.costs.fcdfuel),
)
po.ovarre(
self.outfile,
"Fraction of driver cost --> fuel cost",
"(fcdfuel)",
self.data.costs.fcdfuel,
)
po.oheadr(self.outfile, "Detailed Costings (1990 US$)")
po.ovarre(
self.outfile,
"Acc.22 multiplier for Nth of a kind",
"(fkind)",
self.data.costs.fkind,
)
po.ovarre(
self.outfile, "Level of Safety Assurance", "(lsa)", self.data.costs.lsa
)
po.oblnkl(self.outfile)
po.oshead(self.outfile, "Structures and Site Facilities")
po.ovarre(
self.outfile,
"Site improvements, facilities, land (M$)",
"(c211)",
self.data.costs.c211,
)
po.ovarre(
self.outfile,
"Reactor building cost (M$)",
"(c212)",
self.data.costs.c212,
)
po.ovarre(
self.outfile,
"Turbine building cost (M$)",
"(c213)",
self.data.costs.c213,
)
po.ovarre(
self.outfile,
"Reactor maintenance building cost (M$)",
"(c2141)",
self.data.costs.c2141,
)
po.ovarre(self.outfile, "Warm shop cost (M$)", "(c2142)", self.data.costs.c2142)
po.ovarre(
self.outfile,
"Tritium building cost (M$)",
"(c215)",
self.data.costs.c215,
)
po.ovarre(
self.outfile,
"Electrical equipment building cost (M$)",
"(c216)",
self.data.costs.c216,
)
po.ovarre(
self.outfile,
"Additional buildings cost (M$)",
"(c2171)",
self.data.costs.c2171,
)
po.ovarre(
self.outfile,
"Control room buildings cost (M$)",
"(c2172)",
self.data.costs.c2172,
)
po.ovarre(
self.outfile,
"Shop and warehouses cost (M$)",
"(c2173)",
self.data.costs.c2173,
)
po.ovarre(
self.outfile,
"Cryogenic building cost (M$)",
"(c2174)",
self.data.costs.c2174,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 21 cost (M$)",
"(c21)",
self.data.costs.c21,
)
po.oshead(self.outfile, "Reactor Systems")
po.ovarre(self.outfile, "First wall cost (M$)", "(c2211)", self.data.costs.c2211)
if self.data.ife.ife != 1:
po.ovarre(
self.outfile,
"Blanket beryllium cost (M$)",
"(c22121)",
self.data.costs.c22121,
)
po.ovarre(
self.outfile,
"Blanket breeder material cost (M$)",
"(c22122)",
self.data.costs.c22122,
)
po.ovarre(
self.outfile,
"Blanket stainless steel cost (M$)",
"(c22123)",
self.data.costs.c22123,
)
po.ovarre(
self.outfile,
"Blanket vanadium cost (M$)",
"(c22124)",
self.data.costs.c22124,
)
else: # IFE
po.ovarre(
self.outfile,
"Blanket beryllium cost (M$)",
"(c22121)",
self.data.costs.c22121,
)
po.ovarre(
self.outfile,
"Blanket lithium oxide cost (M$)",
"(c22122)",
self.data.costs.c22122,
)
po.ovarre(
self.outfile,
"Blanket stainless steel cost (M$)",
"(c22123)",
self.data.costs.c22123,
)
po.ovarre(
self.outfile,
"Blanket vanadium cost (M$)",
"(c22124)",
self.data.costs.c22124,
)
po.ovarre(
self.outfile,
"Blanket carbon cloth cost (M$)",
"(c22125)",
self.data.costs.c22125,
)
po.ovarre(
self.outfile,
"Blanket concrete cost (M$)",
"(c22126)",
self.data.costs.c22126,
)
po.ovarre(
self.outfile,
"Blanket FLiBe cost (M$)",
"(c22127)",
self.data.costs.c22127,
)
po.ovarre(
self.outfile,
"Blanket lithium cost (M$)",
"(c22128)",
self.data.costs.c22128,
)
po.ovarre(
self.outfile,
"Blanket total cost (M$)",
"(c2212)",
self.data.costs.c2212,
)
po.ovarre(
self.outfile,
"Bulk shield cost (M$)",
"(c22131)",
self.data.costs.c22131,
)
po.ovarre(
self.outfile,
"Penetration shielding cost (M$)",
"(c22132)",
self.data.costs.c22132,
)
po.ovarre(
self.outfile,
"Total shield cost (M$)",
"(c2213)",
self.data.costs.c2213,
)
po.ovarre(
self.outfile,
"Total support structure cost (M$)",
"(c2214)",
self.data.costs.c2214,
)
po.ovarre(self.outfile, "Divertor cost (M$)", "(c2215)", self.data.costs.c2215)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 221 cost (M$)",
"(c221)",
self.data.costs.c221,
)
if self.data.ife.ife != 1:
po.oshead(self.outfile, "Magnets")
if (
self.data.tfcoil.i_tf_sup != TFConductorModel.SUPERCONDUCTING
): # Resistive TF coils
if self.data.physics.itart == 1:
po.ovarre(
self.outfile,
"Centrepost costs (M$)",
"(c22211)",
self.data.costs.c22211,
)
else:
po.ovarre(
self.outfile,
"Inboard leg cost (M$)",
"(c22211)",
self.data.costs.c22211,
)
po.ovarre(
self.outfile,
"Outboard leg cost (M$)",
"(c22212)",
self.data.costs.c22212,
)
po.ovarre(
self.outfile,
"TF magnet assemblies cost (M$)",
"(c2221)",
self.data.costs.c2221,
)
else: # Superconducting TF coils
po.ovarre(
self.outfile,
"TF coil conductor cost (M$)",
"(c22211)",
self.data.costs.c22211,
)
po.ovarre(
self.outfile,
"TF coil winding cost (M$)",
"(c22212)",
self.data.costs.c22212,
)
po.ovarre(
self.outfile,
"TF coil case cost (M$)",
"(c22213)",
self.data.costs.c22213,
)
po.ovarre(
self.outfile,
"TF intercoil structure cost (M$)",
"(c22214)",
self.data.costs.c22214,
)
po.ovarre(
self.outfile,
"TF coil gravity support structure (M$)",
"(c22215)",
self.data.costs.c22215,
)
po.ovarre(
self.outfile,
"TF magnet assemblies cost (M$)",
"(c2221)",
self.data.costs.c2221,
)
po.ovarre(
self.outfile,
"PF coil conductor cost (M$)",
"(c22221)",
self.data.costs.c22221,
)
po.ovarre(
self.outfile,
"PF coil winding cost (M$)",
"(c22222)",
self.data.costs.c22222,
)
po.ovarre(
self.outfile,
"PF coil case cost (M$)",
"(c22223)",
self.data.costs.c22223,
)
po.ovarre(
self.outfile,
"PF coil support structure cost (M$)",
"(c22224)",
self.data.costs.c22224,
)
po.ovarre(
self.outfile,
"PF magnet assemblies cost (M$)",
"(c2222)",
self.data.costs.c2222,
)
po.ovarre(
self.outfile,
"Vacuum vessel assembly cost (M$)",
"(c2223)",
self.data.costs.c2223,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 222 cost (M$)",
"(c222)",
self.data.costs.c222,
)
po.oshead(self.outfile, "Power Injection")
if self.data.ife.ife == 1:
po.ovarre(
self.outfile,
"IFE driver system cost (M$)",
"(c2231)",
self.data.costs.c2231,
)
else:
po.ovarre(
self.outfile,
"ECH system cost (M$)",
"(c2231)",
self.data.costs.c2231,
)
po.ovarre(
self.outfile,
"Lower hybrid system cost (M$)",
"(c2232)",
self.data.costs.c2232,
)
po.ovarre(
self.outfile,
"Neutral beam system cost (M$)",
"(c2233)",
self.data.costs.c2233,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 223 cost (M$)",
"(c223)",
self.data.costs.c223,
)
po.oshead(self.outfile, "Vacuum Systems")
po.ovarre(
self.outfile,
"High vacuum pumps cost (M$)",
"(c2241)",
self.data.costs.c2241,
)
po.ovarre(
self.outfile,
"Backing pumps cost (M$)",
"(c2242)",
self.data.costs.c2242,
)
po.ovarre(
self.outfile,
"Vacuum duct cost (M$)",
"(c2243)",
self.data.costs.c2243,
)
po.ovarre(self.outfile, "Valves cost (M$)", "(c2244)", self.data.costs.c2244)
po.ovarre(
self.outfile,
"Duct shielding cost (M$)",
"(c2245)",
self.data.costs.c2245,
)
po.ovarre(
self.outfile,
"Instrumentation cost (M$)",
"(c2246)",
self.data.costs.c2246,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 224 cost (M$)",
"(c224)",
self.data.costs.c224,
)
if self.data.ife.ife != 1:
po.oshead(self.outfile, "Power Conditioning")
po.ovarre(
self.outfile,
"TF coil power supplies cost (M$)",
"(c22511)",
self.data.costs.c22511,
)
po.ovarre(
self.outfile,
"TF coil breakers cost (M$)",
"(c22512)",
self.data.costs.c22512,
)
po.ovarre(
self.outfile,
"TF coil dump resistors cost (M$)",
"(c22513)",
self.data.costs.c22513,
)
po.ovarre(
self.outfile,
"TF coil instrumentation and control (M$)",
"(c22514)",
self.data.costs.c22514,
)
po.ovarre(
self.outfile,
"TF coil bussing cost (M$)",
"(c22515)",
self.data.costs.c22515,
)
po.ovarre(
self.outfile,
"Total, TF coil power costs (M$)",
"(c2251)",
self.data.costs.c2251,
)
po.ovarre(
self.outfile,
"PF coil power supplies cost (M$)",
"(c22521)",
self.data.costs.c22521,
)
po.ovarre(
self.outfile,
"PF coil instrumentation and control (M$)",
"(c22522)",
self.data.costs.c22522,
)
po.ovarre(
self.outfile,
"PF coil bussing cost (M$)",
"(c22523)",
self.data.costs.c22523,
)
po.ovarre(
self.outfile,
"PF coil burn power supplies cost (M$)",
"(c22524)",
self.data.costs.c22524,
)
po.ovarre(
self.outfile,
"PF coil breakers cost (M$)",
"(c22525)",
self.data.costs.c22525,
)
po.ovarre(
self.outfile,
"PF coil dump resistors cost (M$)",
"(c22526)",
self.data.costs.c22526,
)
po.ovarre(
self.outfile,
"PF coil ac breakers cost (M$)",
"(c22527)",
self.data.costs.c22527,
)
po.ovarre(
self.outfile,
"Total, PF coil power costs (M$)",
"(c2252)",
self.data.costs.c2252,
)
po.ovarre(
self.outfile,
"Total, energy storage cost (M$)",
"(c2253)",
self.data.costs.c2253,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 225 cost (M$)",
"(c225)",
self.data.costs.c225,
)
po.oshead(self.outfile, "Heat Transport System")
po.ovarre(
self.outfile,
"Pumps and piping system cost (M$)",
"(cpp)",
self.data.costs.cpp,
)
po.ovarre(
self.outfile,
"Primary heat exchanger cost (M$)",
"(chx)",
self.data.costs.chx,
)
po.ovarre(
self.outfile,
"Total, reactor cooling system cost (M$)",
"(c2261)",
self.data.costs.c2261,
)
po.ovarre(
self.outfile,
"Pumps, piping cost (M$)",
"(cppa)",
self.data.costs.cppa,
)
po.ovarre(
self.outfile,
"Total, auxiliary cooling system cost (M$)",
"(c2262)",
self.data.costs.c2262,
)
po.ovarre(
self.outfile,
"Total, cryogenic system cost (M$)",
"(c2263)",
self.data.costs.c2263,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 226 cost (M$)",
"(c226)",
self.data.costs.c226,
)
po.oshead(self.outfile, "Fuel Handling System")
po.ovarre(
self.outfile,
"Fuelling system cost (M$)",
"(c2271)",
self.data.costs.c2271,
)
po.ovarre(
self.outfile,
"Fuel processing and purification cost (M$)",
"(c2272)",
self.data.costs.c2272,
)
po.ovarre(
self.outfile,
"Atmospheric recovery systems cost (M$)",
"(c2273)",
self.data.costs.c2273,
)
po.ovarre(
self.outfile,
"Nuclear building ventilation cost (M$)",
"(c2274)",
self.data.costs.c2274,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 227 cost (M$)",
"(c227)",
self.data.costs.c227,
)
po.oshead(self.outfile, "Instrumentation and Control")
po.ovarre(
self.outfile,
"Instrumentation and control cost (M$)",
"(c228)",
self.data.costs.c228,
)
po.oshead(self.outfile, "Maintenance Equipment")
po.ovarre(
self.outfile,
"Maintenance equipment cost (M$)",
"(c229)",
self.data.costs.c229,
)
po.oshead(self.outfile, "Total Account 22 Cost")
po.ovarre(
self.outfile,
"Total account 22 cost (M$)",
"(c22)",
self.data.costs.c22,
)
po.oshead(self.outfile, "Turbine Plant Equipment")
po.ovarre(
self.outfile,
"Turbine plant equipment cost (M$)",
"(c23)",
self.data.costs.c23,
)
po.oshead(self.outfile, "Electric Plant Equipment")
po.ovarre(
self.outfile,
"Switchyard equipment cost (M$)",
"(c241)",
self.data.costs.c241,
)
po.ovarre(self.outfile, "Transformers cost (M$)", "(c242)", self.data.costs.c242)
po.ovarre(
self.outfile,
"Low voltage equipment cost (M$)",
"(c243)",
self.data.costs.c243,
)
po.ovarre(
self.outfile,
"Diesel backup equipment cost (M$)",
"(c244)",
self.data.costs.c244,
)
po.ovarre(
self.outfile,
"Auxiliary facilities cost (M$)",
"(c245)",
self.data.costs.c245,
)
po.oblnkl(self.outfile)
po.ovarre(
self.outfile,
"Total account 24 cost (M$)",
"(c24)",
self.data.costs.c24,
)
po.oshead(self.outfile, "Miscellaneous Plant Equipment")
po.ovarre(
self.outfile,
"Miscellaneous plant equipment cost (M$)",
"(c25)",
self.data.costs.c25,
)
po.oshead(self.outfile, "Heat Rejection System")
po.ovarre(
self.outfile,
"Heat rejection system cost (M$)",
"(c26)",
self.data.costs.c26,
)
po.oshead(self.outfile, "Plant Direct Cost")
po.ovarre(
self.outfile, "Plant direct cost (M$)", "(cdirt)", self.data.costs.cdirt
)
po.oshead(self.outfile, "Reactor Core Cost")
po.ovarre(
self.outfile,
"Reactor core cost (M$)",
"(crctcore)",
self.data.costs.crctcore,
)
po.oshead(self.outfile, "Indirect Cost")
po.ovarre(self.outfile, "Indirect cost (M$)", "(c9)", self.data.costs.cindrt)
po.oshead(self.outfile, "Total Contingency")
po.ovarre(
self.outfile,
"Total contingency (M$)",
"(ccont)",
self.data.costs.ccont,
)
po.oshead(self.outfile, "Constructed Cost")
po.ovarre(
self.outfile,
"Constructed cost (M$)",
"(concost)",
self.data.costs.concost,
)
if self.data.costs.ireactor == 1:
po.oshead(self.outfile, "Interest during Construction")
po.ovarre(
self.outfile,
"Interest during construction (M$)",
"(moneyint)",
self.data.costs.moneyint,
)
po.oshead(self.outfile, "Total Capital Investment")
po.ovarre(
self.outfile,
"Total capital investment (M$)",
"(capcost)",
self.data.costs.capcost,
)
def acc22(self):
"""Account 22 : Fusion power island
This routine evaluates the Account 22 (fusion power island
- the tokamak itself plus auxiliary power systems, etc.) costs.
"""
self.acc221()
# Account 222 : Magnets
self.acc222()
# Account 223 : Power injection
self.acc223()
# Account 224 : Vacuum system
self.acc224()
# Account 225 : Power conditioning
self.acc225()
# Account 226 : Heat transport system
self.acc2261() # Account 2261 : Reactor cooling system
self.acc2262() # Account 2262 : Auxiliary component coolin
self.acc2263() # Account 2263 : Cryogenic system
self.acc226() # ccount 226 : Total
# Account 227 : Fuel handling
self.acc2271() # Account 2271 : Fuelling system
self.acc2272() # Account 2272 : Fuel processing and purification
self.acc2273() # Account 2273 : Atmospheric recovery systems
self.acc2274() # Account 2274 : Nuclear building ventilation
self.acc227() # Account 227 : Total
# Account 228 : Instrumentation and control
self.acc228()
# Account 229 : Maintenance equipment
self.acc229()
# Reactor core costs
self.data.costs.crctcore = (
self.data.costs.c221 + self.data.costs.c222 + self.data.costs.c223
)
# Total account 22
self.data.costs.c22 = (
self.data.costs.c221
+ self.data.costs.c222
+ self.data.costs.c223
+ self.data.costs.c224
+ self.data.costs.c225
+ self.data.costs.c226
+ self.data.costs.c227
+ self.data.costs.c228
+ self.data.costs.c229
)
def acc221(self):
"""Account 221 : Reactor
This routine evaluates the Account 221 (reactor) costs.
These include the first wall, blanket, shield, support structure
and divertor plates.
<P>If ifueltyp = 1, the first wall, blanket and divertor costs are
treated as fuel costs, rather than as capital costs.
<P>If ifueltyp = 2, the initial first wall, blanket and divertor costs are
treated as capital costs, and replacemnts are included as fuel costs.
"""
self.acc2211()
# Account 221.2 : Blanket
self.acc2212()
# Account 221.3 : Shield
self.acc2213()
# Account 221.4 : Reactor structure
self.acc2214()
# Account 221.5 : Divertor
self.acc2215()
# Total account 221
self.data.costs.c221 = (
self.data.costs.c2211
+ self.data.costs.c2212
+ self.data.costs.c2213
+ self.data.costs.c2214
+ self.data.costs.c2215
)
def acc222(self):
"""Account 222 : Magnets, including cryostat
This routine evaluates the Account 222 (magnet) costs,
including the costs of associated cryostats.
"""
if self.data.ife.ife == 1:
self.data.costs.c222 = 0.0e0
return
# Account 222.1 : TF magnet assemblies
self.acc2221()
# Account 222.2 : PF magnet assemblies
self.acc2222()
# Account 222.3 : Cryostat
self.acc2223()
# Total account 222
self.data.costs.c222 = (
self.data.costs.c2221 + self.data.costs.c2222 + self.data.costs.c2223
)
def acc225(self):
"""Account 225 : Power conditioning
This routine evaluates the Account 225 (power conditioning) costs.
"""
if self.data.ife.ife == 1:
self.data.costs.c225 = 0.0e0
else:
# Account 225.1 : TF coil power conditioning
self.acc2251()
# Account 225.2 : PF coil power conditioning
self.acc2252()
# Account 225.3 : Energy storage
self.acc2253()
# Total account 225
self.data.costs.c225 = (
self.data.costs.c2251 + self.data.costs.c2252 + self.data.costs.c2253
)
def acc21(self):
"""Account 21 : Structures and site facilities
This routine evaluates the Account 21 (structures and site
facilities) costs.
Building costs are scaled with volume according to algorithms
developed from TFCX, TFTR, and commercial power plant buildings.
Costs include equipment, materials and installation labour, but
no engineering or construction management.
<P>The general form of the cost algorithm is cost=ucxx*volume**expxx.
Allowances are used for site improvements and for miscellaneous
buildings and land costs.
"""
cmlsa = [0.6800e0, 0.8400e0, 0.9200e0, 1.0000e0]
exprb = 1.0e0
# Account 211 : Site improvements, facilities and land
# N.B. Land unaffected by LSA
self.data.costs.c211 = (
self.data.costs.csi * cmlsa[self.data.costs.lsa - 1] + self.data.costs.cland
)
# Account 212 : Reactor building
self.data.costs.c212 = (
1.0e-6
* self.data.costs.ucrb
* self.data.buildings.rbvol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
# Account 213 : Turbine building
if self.data.costs.ireactor == 1:
self.data.costs.c213 = (
self.data.costs.cturbb * cmlsa[self.data.costs.lsa - 1]
)
else:
self.data.costs.c213 = 0.0e0
# Account 214 : Reactor maintenance and warm shops buildings
self.data.costs.c2141 = (
1.0e-6
* self.data.costs.UCMB
* self.data.buildings.rmbvol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2142 = (
1.0e-6
* self.data.costs.UCWS
* self.data.buildings.wsvol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c214 = self.data.costs.c2141 + self.data.costs.c2142
# Account 215 : Tritium building
self.data.costs.c215 = (
1.0e-6
* self.data.costs.UCTR
* self.data.buildings.triv**exprb
* cmlsa[self.data.costs.lsa - 1]
)
# Account 216 : Electrical equipment building
self.data.costs.c216 = (
1.0e-6
* self.data.costs.UCEL
* self.data.buildings.elevol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
# Account 217 : Other buildings
# Includes administration, control, shops, cryogenic
# plant and an allowance for miscellaneous structures
self.data.costs.c2171 = (
1.0e-6
* self.data.costs.UCAD
* self.data.buildings.admvol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2172 = (
1.0e-6
* self.data.costs.UCCO
* self.data.buildings.convol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2173 = (
1.0e-6
* self.data.costs.UCSH
* self.data.buildings.shovol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2174 = (
1.0e-6
* self.data.costs.UCCR
* self.data.buildings.cryvol**exprb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c217 = (
self.data.costs.c2171
+ self.data.costs.c2172
+ self.data.costs.c2173
+ self.data.costs.c2174
)
# Total for Account 21
self.data.costs.c21 = (
self.data.costs.c211
+ self.data.costs.c212
+ self.data.costs.c213
+ self.data.costs.c214
+ self.data.costs.c215
+ self.data.costs.c216
+ self.data.costs.c217
)
def acc2211(self):
"""Account 221.1 : First wall
This routine evaluates the Account 221.1 (first wall) costs.
The first wall cost is scaled linearly with surface area from TFCX.
If ifueltyp = 1, the first wall cost is treated as a fuel cost,
rather than as a capital cost.
If ifueltyp = 2, initial first wall is included as a capital cost,
and the replacement first wall cost is treated as a fuel costs.
"""
cmlsa = [0.5000e0, 0.7500e0, 0.8750e0, 1.0000e0]
if self.data.ife.ife != 1:
self.data.costs.c2211 = (
1.0e-6
* cmlsa[self.data.costs.lsa - 1]
* (
(self.data.costs.UCFWA + self.data.costs.UCFWS)
* self.data.first_wall.a_fw_total
+ self.data.costs.UCFWPS
)
)
else:
self.data.costs.c2211 = (
1.0e-6
* cmlsa[self.data.costs.lsa - 1]
* (
self.data.costs.ucblss
* (
self.data.ife.fwmatm[0, 0]
+ self.data.ife.fwmatm[1, 0]
+ self.data.ife.fwmatm[2, 0]
)
+ self.data.ife.uccarb
* (
self.data.ife.fwmatm[0, 1]
+ self.data.ife.fwmatm[1, 1]
+ self.data.ife.fwmatm[2, 1]
)
+ self.data.costs.ucblli2o
* (
self.data.ife.fwmatm[0, 3]
+ self.data.ife.fwmatm[1, 3]
+ self.data.ife.fwmatm[2, 3]
)
+ self.data.ife.ucconc
* (
self.data.ife.fwmatm[0, 4]
+ self.data.ife.fwmatm[1, 4]
+ self.data.ife.fwmatm[2, 4]
)
)
)
self.data.costs.c2211 = self.data.costs.fkind * self.data.costs.c2211
if self.data.costs.ifueltyp == 1:
self.data.costs.fwallcst = self.data.costs.c2211
self.data.costs.c2211 = 0.0e0
elif self.data.costs.ifueltyp == 2:
self.data.costs.fwallcst = self.data.costs.c2211
else:
self.data.costs.fwallcst = 0.0e0
def acc2212(self):
"""Account 221.2 : Blanket
This routine evaluates the Account 221.2 (blanket) costs.
If ifueltyp = 1, the blanket cost is treated as a fuel cost,
rather than as a capital cost.
If ifueltyp = 2, the initial blanket is included as a capital cost
and the replacement blanket costs are treated as a fuel cost.
"""
cmlsa = [0.5000e0, 0.7500e0, 0.8750e0, 1.0000e0]
if self.data.ife.ife != 1:
# Solid blanket (Li2O + Be)
self.data.costs.c22121 = (
1.0e-6 * self.data.fwbs.m_blkt_beryllium * self.data.costs.ucblbe
)
# CCFE model
self.data.costs.c22122 = (
1.0e-6 * self.data.fwbs.m_blkt_li2o * self.data.costs.ucblli2o
)
self.data.costs.c22123 = (
1.0e-6 * self.data.fwbs.m_blkt_steel_total * self.data.costs.ucblss
)
self.data.costs.c22124 = (
1.0e-6 * self.data.fwbs.m_blkt_vanadium * self.data.costs.ucblvd
)
self.data.costs.c22125 = 0.0e0
self.data.costs.c22126 = 0.0e0
self.data.costs.c22127 = 0.0e0
else:
# IFE blanket; materials present are Li2O, steel, carbon, concrete,
# FLiBe and lithium
self.data.costs.c22121 = 0.0e0
self.data.costs.c22122 = (
1.0e-6 * self.data.fwbs.m_blkt_li2o * self.data.costs.ucblli2o
)
self.data.costs.c22123 = (
1.0e-6 * self.data.fwbs.m_blkt_steel_total * self.data.costs.ucblss
)
self.data.costs.c22124 = 0.0e0
self.data.costs.c22125 = (
1.0e-6
* self.data.ife.uccarb
* (
self.data.ife.blmatm[0, 1]
+ self.data.ife.blmatm[1, 1]
+ self.data.ife.blmatm[2, 1]
)
)
self.data.costs.c22126 = (
1.0e-6
* self.data.ife.ucconc
* (
self.data.ife.blmatm[0, 4]
+ self.data.ife.blmatm[1, 4]
+ self.data.ife.blmatm[2, 4]
)
)
self.data.costs.c22127 = 1.0e-6 * self.data.ife.ucflib * self.data.ife.mflibe
self.data.costs.c22128 = (
1.0e-6 * self.data.costs.ucblli * self.data.fwbs.m_blkt_lithium
)
self.data.costs.c22121 = (
self.data.costs.fkind
* self.data.costs.c22121
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22122 = (
self.data.costs.fkind
* self.data.costs.c22122
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22123 = (
self.data.costs.fkind
* self.data.costs.c22123
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22124 = (
self.data.costs.fkind
* self.data.costs.c22124
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22125 = (
self.data.costs.fkind
* self.data.costs.c22125
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22126 = (
self.data.costs.fkind
* self.data.costs.c22126
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22127 = (
self.data.costs.fkind
* self.data.costs.c22127
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2212 = (
self.data.costs.c22121
+ self.data.costs.c22122
+ self.data.costs.c22123
+ self.data.costs.c22124
+ self.data.costs.c22125
+ self.data.costs.c22126
+ self.data.costs.c22127
)
if self.data.costs.ifueltyp == 1:
self.data.costs.blkcst = self.data.costs.c2212
self.data.costs.c2212 = 0.0e0
elif self.data.costs.ifueltyp == 2:
self.data.costs.blkcst = self.data.costs.c2212
else:
self.data.costs.blkcst = 0.0e0
def acc2213(self):
"""Account 221.3 : Shield
This routine evaluates the Account 221.3 (shield) costs.
"""
cmlsa = [0.5000e0, 0.7500e0, 0.8750e0, 1.0000e0]
if self.data.ife.ife != 1:
self.data.costs.c22131 = (
1.0e-6
* self.data.fwbs.whtshld
* self.data.costs.ucshld
* cmlsa[self.data.costs.lsa - 1]
)
else:
self.data.costs.c22131 = (
1.0e-6
* cmlsa[self.data.costs.lsa - 1]
* (
self.data.costs.ucshld
* (
self.data.ife.shmatm[0, 0]
+ self.data.ife.shmatm[1, 0]
+ self.data.ife.shmatm[2, 0]
)
+ self.data.ife.uccarb
* (
self.data.ife.shmatm[0, 1]
+ self.data.ife.shmatm[1, 1]
+ self.data.ife.shmatm[2, 1]
)
+ self.data.costs.ucblli2o
* (
self.data.ife.shmatm[0, 3]
+ self.data.ife.shmatm[1, 3]
+ self.data.ife.shmatm[2, 3]
)
+ self.data.ife.ucconc
* (
self.data.ife.shmatm[0, 4]
+ self.data.ife.shmatm[1, 4]
+ self.data.ife.shmatm[2, 4]
)
)
)
self.data.costs.c22131 = self.data.costs.fkind * self.data.costs.c22131
# Penetration shield assumed to be typical steel plate
if self.data.ife.ife != 1:
self.data.costs.c22132 = (
1.0e-6
* self.data.fwbs.wpenshld
* self.data.costs.ucpens
* cmlsa[self.data.costs.lsa - 1]
)
else:
self.data.costs.c22132 = 0.0e0
self.data.costs.c22132 = self.data.costs.fkind * self.data.costs.c22132
self.data.costs.c2213 = self.data.costs.c22131 + self.data.costs.c22132
def acc2214(self):
"""Account 221.4 : Reactor structure
This routine evaluates the Account 221.4 (reactor structure) costs.
The structural items are costed as standard steel elements.
"""
cmlsa = [0.6700e0, 0.8350e0, 0.9175e0, 1.0000e0]
self.data.costs.c2214 = (
1.0e-6
* self.data.structure.gsmass
* self.data.costs.UCGSS
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2214 = self.data.costs.fkind * self.data.costs.c2214
def acc2215(self):
"""Account 221.5 : Divertor
This routine evaluates the Account 221.5 (divertor) costs.
The cost of the divertor blade is scaled linearly with
surface area from TFCX. The graphite armour is assumed to
be brazed to water-cooled machined copper substrate.
Tenth-of-a-kind engineering and installation is assumed.
<P>If ifueltyp = 1, the divertor cost is treated as a fuel cost,
rather than as a capital cost.
<P>If ifueltyp = 2, the initial divertor is included as a capital cost
and the replacement divertor costs ae treated as a fuel cost,
"""
if self.data.ife.ife != 1:
self.data.costs.c2215 = (
1.0e-6 * self.data.divertor.a_div_surface_total * self.data.costs.ucdiv
)
self.data.costs.c2215 = self.data.costs.fkind * self.data.costs.c2215
if self.data.costs.ifueltyp == 1:
self.data.costs.divcst = self.data.costs.c2215
self.data.costs.c2215 = 0.0e0
elif self.data.costs.ifueltyp == 2:
self.data.costs.divcst = self.data.costs.c2215
else:
self.data.costs.divcst = 0.0e0
else:
self.data.costs.c2215 = 0.0e0
self.data.costs.divcst = 0.0e0
def acc2221(self):
"""Account 222.1 : TF magnet assemblies
This routine evaluates the Account 222.1 (TF magnet) costs.
Copper magnets are costed from the TFCX data base ($/kg).
Superconductor magnets are costed using a new method devised
by R. Hancox under contract to Culham Laboratory, Jan/Feb 1994.
If ifueltyp = 1, the TART centrepost cost is treated as a fuel
cost, rather than as a capital cost.
If ifueltyp = 2, the initial centrepost is included as a capital cost
and the replacement TART centrepost costs are treated as a fuel
"""
cmlsa = [0.6900e0, 0.8450e0, 0.9225e0, 1.0000e0]
if (
self.data.tfcoil.i_tf_sup != TFConductorModel.SUPERCONDUCTING
): # Resistive TF coils
# Account 222.1.1 : Inboard TF coil legs
self.data.costs.c22211 = (
1.0e-6
* self.data.tfcoil.whtcp
* self.data.costs.uccpcl1
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22211 = self.data.costs.fkind * self.data.costs.c22211
self.data.costs.cpstcst = 0.0e0 # TART centrepost
if (self.data.physics.itart == 1) and (self.data.costs.ifueltyp == 1):
self.data.costs.cpstcst = self.data.costs.c22211
self.data.costs.c22211 = 0.0e0
elif (self.data.physics.itart == 1) and (self.data.costs.ifueltyp == 2):
self.data.costs.cpstcst = self.data.costs.c22211
# Account 222.1.2 : Outboard TF coil legs
self.data.costs.c22212 = (
1.0e-6
* self.data.tfcoil.whttflgs
* self.data.costs.uccpclb
* cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c22212 = self.data.costs.fkind * self.data.costs.c22212
# Total (copper) TF coil costs
self.data.costs.c2221 = self.data.costs.c22211 + self.data.costs.c22212
else: # Superconducting TF coils
# Account 222.1.1 : Conductor
# Superconductor ($/m)
if self.data.costs.supercond_cost_model == 0:
costtfsc = (
self.data.costs.ucsc[self.data.tfcoil.i_tf_sc_mat - 1]
* self.data.tfcoil.m_tf_coil_superconductor
/ (self.data.tfcoil.len_tf_coil * self.data.tfcoil.n_tf_coil_turns)
)
else:
costtfsc = (
self.data.costs.sc_mat_cost_0[self.data.tfcoil.i_tf_sc_mat - 1]
* self.data.tfcoil.j_crit_str_0[self.data.tfcoil.i_tf_sc_mat - 1]
/ self.data.tfcoil.j_crit_str_tf
)
# Copper ($/m)
costtfcu = (
self.data.costs.uccu
* self.data.tfcoil.m_tf_coil_copper
/ (self.data.tfcoil.len_tf_coil * self.data.tfcoil.n_tf_coil_turns)
)
# Total cost/metre of superconductor and copper wire
costwire = costtfsc + costtfcu
# Total cost/metre of conductor (including sheath and fixed costs)
ctfconpm = costwire + self.data.costs.cconshtf + self.data.costs.cconfix
# Total conductor costs
self.data.costs.c22211 = (
1.0e-6
* ctfconpm
* self.data.tfcoil.n_tf_coils
* self.data.tfcoil.len_tf_coil
* self.data.tfcoil.n_tf_coil_turns
)
self.data.costs.c22211 = (
self.data.costs.fkind
* self.data.costs.c22211
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.1.2 : Winding
self.data.costs.c22212 = (
1.0e-6
* self.data.costs.ucwindtf
* self.data.tfcoil.n_tf_coils
* self.data.tfcoil.len_tf_coil
* self.data.tfcoil.n_tf_coil_turns
)
self.data.costs.c22212 = (
self.data.costs.fkind
* self.data.costs.c22212
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.1.3 : Case
self.data.costs.c22213 = (
1.0e-6
* (self.data.tfcoil.m_tf_coil_case * self.data.costs.uccase)
* self.data.tfcoil.n_tf_coils
)
self.data.costs.c22213 = (
self.data.costs.fkind
* self.data.costs.c22213
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.1.4 : Intercoil structure
self.data.costs.c22214 = (
1.0e-6 * self.data.structure.aintmass * self.data.costs.UCINT
)
self.data.costs.c22214 = (
self.data.costs.fkind
* self.data.costs.c22214
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.1.5 : Gravity support structure
self.data.costs.c22215 = (
1.0e-6 * self.data.structure.clgsmass * self.data.costs.UCGSS
)
self.data.costs.c22215 = (
self.data.costs.fkind
* self.data.costs.c22215
* cmlsa[self.data.costs.lsa - 1]
)
# Total (superconducting) TF coil costs
self.data.costs.c2221 = (
self.data.costs.c22211
+ self.data.costs.c22212
+ self.data.costs.c22213
+ self.data.costs.c22214
+ self.data.costs.c22215
)
def acc2222(self):
"""Account 222.2 : PF magnet assemblies
This routine evaluates the Account 222.2 (PF magnet) costs.
Conductor costs previously used an algorithm devised by R. Hancox,
January 1994, under contract to Culham, which took into
account the fact that the superconductor/copper ratio in
the conductor is proportional to the maximum field that
each coil will experience. Now, the input copper fractions
are used instead.
Maximum values for current, current density and field
are used.
"""
cmlsa = [0.6900e0, 0.8450e0, 0.9225e0, 1.0000e0]
# Total length of PF coil windings (m)
pfwndl = 0.0e0
for i in range(self.data.pf_coil.n_cs_pf_coils):
pfwndl += (
2.0
* np.pi
* self.data.pf_coil.r_pf_coil_middle[i]
* self.data.pf_coil.n_pf_coil_turns[i]
)
# Account 222.2.1 : Conductor
# The following lines take care of resistive coils.
# costpfsh is the cost per metre of the steel conduit/sheath around
# each superconducting cable (so is zero for resistive coils)
costpfsh = (
0.0
if self.data.pf_coil.i_pf_conductor == PFConductorModel.RESISTIVE
else self.data.costs.cconshpf
)
# Non-Central Solenoid coils
if self.data.build.iohcl == 1:
npf = self.data.pf_coil.n_cs_pf_coils - 1
else:
npf = self.data.pf_coil.n_cs_pf_coils
self.data.costs.c22221 = 0.0e0
for i in range(npf):
# Superconductor ($/m)
if self.data.costs.supercond_cost_model == 0:
if self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfsc = (
self.data.costs.ucsc[self.data.pf_coil.i_pf_superconductor - 1]
* (1.0e0 - self.data.pf_coil.fcupfsu)
* (1.0e0 - self.data.pf_coil.f_a_pf_coil_void[i])
* abs(
self.data.pf_coil.c_pf_cs_coils_peak_ma[i]
/ self.data.pf_coil.n_pf_coil_turns[i]
)
* 1.0e6
/ self.data.pf_coil.j_pf_coil_wp_peak[i]
* self.data.tfcoil.dcond[
self.data.pf_coil.i_pf_superconductor - 1
]
)
else:
costpfsc = 0.0e0
elif self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfsc = (
self.data.costs.sc_mat_cost_0[
self.data.pf_coil.i_pf_superconductor - 1
]
* self.data.tfcoil.j_crit_str_0[
self.data.pf_coil.i_pf_superconductor - 1
]
/ self.data.pf_coil.j_crit_str_pf
)
else:
costpfsc = 0.0
# Copper ($/m)
if self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfcu = (
self.data.costs.uccu
* self.data.pf_coil.fcupfsu
* (1.0e0 - self.data.pf_coil.f_a_pf_coil_void[i])
* abs(
self.data.pf_coil.c_pf_cs_coils_peak_ma[i]
/ self.data.pf_coil.n_pf_coil_turns[i]
)
* 1.0e6
/ self.data.pf_coil.j_pf_coil_wp_peak[i]
* constants.DEN_COPPER
)
else:
costpfcu = (
self.data.costs.uccu
* (1.0e0 - self.data.pf_coil.f_a_pf_coil_void[i])
* abs(
self.data.pf_coil.c_pf_cs_coils_peak_ma[i]
/ self.data.pf_coil.n_pf_coil_turns[i]
)
* 1.0e6
/ self.data.pf_coil.j_pf_coil_wp_peak[i]
* constants.DEN_COPPER
)
# Total cost/metre of superconductor and copper wire
costwire = costpfsc + costpfcu
# Total cost/metre of conductor (including sheath and fixed costs)
cpfconpm = costwire + costpfsh + self.data.costs.cconfix
# Total account 222.2.1 (PF coils excluding Central Solenoid)
self.data.costs.c22221 += (
1.0e-6
* 2.0
* np.pi
* self.data.pf_coil.r_pf_coil_middle[i]
* self.data.pf_coil.n_pf_coil_turns[i]
* cpfconpm
)
# Central Solenoid
if self.data.build.iohcl == 1:
# Superconductor ($/m)
if self.data.costs.supercond_cost_model == 0:
# Issue #328 Use CS conductor cross-sectional area (m2)
if self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfsc = (
self.data.costs.ucsc[self.data.pf_coil.i_cs_superconductor - 1]
* self.data.pf_coil.a_cs_cable_space
* (1 - self.data.pf_coil.f_a_cs_void)
* (1 - self.data.pf_coil.fcuohsu)
/ self.data.pf_coil.n_pf_coil_turns[
self.data.pf_coil.n_cs_pf_coils - 1
]
* self.data.tfcoil.dcond[
self.data.pf_coil.i_cs_superconductor - 1
]
)
else:
costpfsc = 0.0e0
elif self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfsc = (
self.data.costs.sc_mat_cost_0[
self.data.pf_coil.i_cs_superconductor - 1
]
* self.data.tfcoil.j_crit_str_0[
self.data.pf_coil.i_cs_superconductor - 1
]
/ self.data.pf_coil.j_crit_str_cs
)
else:
costpfsc = 0.0e0
# Copper ($/m)
if self.data.pf_coil.i_pf_conductor == PFConductorModel.SUPERCONDUCTING:
costpfcu = (
self.data.costs.uccu
* self.data.pf_coil.a_cs_cable_space
* (1 - self.data.pf_coil.f_a_cs_void)
* self.data.pf_coil.fcuohsu
/ self.data.pf_coil.n_pf_coil_turns[
self.data.pf_coil.n_cs_pf_coils - 1
]
* constants.DEN_COPPER
)
else:
# MDK I don't know if this is ccorrect as we never use the
# resistive model
costpfcu = (
self.data.costs.uccu
* self.data.pf_coil.a_cs_cable_space
* (1 - self.data.pf_coil.f_a_cs_void)
/ self.data.pf_coil.n_pf_coil_turns[
self.data.pf_coil.n_cs_pf_coils - 1
]
* constants.DEN_COPPER
)
# Total cost/metre of superconductor and copper wire (Central Solenoid)
costwire = costpfsc + costpfcu
# Total cost/metre of conductor (including sheath and fixed costs)
cpfconpm = costwire + costpfsh + self.data.costs.cconfix
# Total account 222.2.1 (PF+Central Solenoid coils)
self.data.costs.c22221 += (
1.0e-6
* 2.0
* np.pi
* self.data.pf_coil.r_pf_coil_middle[self.data.pf_coil.n_cs_pf_coils - 1]
* self.data.pf_coil.n_pf_coil_turns[self.data.pf_coil.n_cs_pf_coils - 1]
* cpfconpm
)
self.data.costs.c22221 = (
self.data.costs.fkind
* self.data.costs.c22221
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.2.2 : Winding
self.data.costs.c22222 = 1.0e-6 * self.data.costs.ucwindpf * pfwndl
self.data.costs.c22222 = (
self.data.costs.fkind
* self.data.costs.c22222
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.2.3 : Steel case - will be zero for resistive coils
self.data.costs.c22223 = (
1.0e-6 * self.data.costs.uccase * self.data.pf_coil.m_pf_coil_structure_total
)
self.data.costs.c22223 = (
self.data.costs.fkind
* self.data.costs.c22223
* cmlsa[self.data.costs.lsa - 1]
)
# Account 222.2.4 : Support structure
self.data.costs.c22224 = (
1.0e-6 * self.data.costs.ucfnc * self.data.structure.fncmass
)
self.data.costs.c22224 = (
self.data.costs.fkind
* self.data.costs.c22224
* cmlsa[self.data.costs.lsa - 1]
)
# Total account 222.2
self.data.costs.c2222 = (
self.data.costs.c22221
+ self.data.costs.c22222
+ self.data.costs.c22223
+ self.data.costs.c22224
)
def acc2223(self):
"""Account 222.3 : Vacuum vessel
This routine evaluates the Account 222.3 (vacuum vessel) costs.
"""
cmlsa = [0.6900e0, 0.8450e0, 0.9225e0, 1.0000e0]
self.data.costs.c2223 = 1.0e-6 * self.data.fwbs.m_vv * self.data.costs.uccryo
self.data.costs.c2223 = (
self.data.costs.fkind
* self.data.costs.c2223
* cmlsa[self.data.costs.lsa - 1]
)
def acc223(self):
"""Account 223 : Power injection
This routine evaluates the Account 223 (power injection) costs.
The costs are from TETRA, updated to 1990$.
Nominal TIBER values are used pending system designs. Costs are
scaled linearly with power injected into the plasma and include
the power supplies.
<P>If ifueltyp=1, the fraction (1-fcdfuel) of the cost of the
current drive system is considered as capital cost, and the
fraction (fcdfuel) is considered a recurring fuel cost due
to the system's short life.
"""
exprf = 1.0e0
if self.data.ife.ife != 1:
# Account 223.1 : ECH
self.data.costs.c2231 = (
1.0e-6
* self.data.costs.ucech
* (1.0e6 * self.data.current_drive.p_hcd_ecrh_injected_total_mw) ** exprf
)
if self.data.costs.ifueltyp == 1:
self.data.costs.c2231 = (
1.0e0 - self.data.costs.fcdfuel
) * self.data.costs.c2231
self.data.costs.c2231 = self.data.costs.fkind * self.data.costs.c2231
# Account 223.2 : Lower Hybrid or ICH
if self.data.current_drive.i_hcd_primary != 2:
self.data.costs.c2232 = (
1.0e-6
* self.data.costs.uclh
* (1.0e6 * self.data.current_drive.p_hcd_lowhyb_injected_total_mw)
** exprf
)
else:
self.data.costs.c2232 = (
1.0e-6
* self.data.costs.ucich
* (1.0e6 * self.data.current_drive.p_hcd_lowhyb_injected_total_mw)
** exprf
)
if self.data.costs.ifueltyp == 1:
self.data.costs.c2232 = (
1.0e0 - self.data.costs.fcdfuel
) * self.data.costs.c2232
self.data.costs.c2232 = self.data.costs.fkind * self.data.costs.c2232
# Account 223.3 : Neutral Beam
# self.data.costs.c2233 =
# 1.0e-6 * self.data.costs.ucnbi
# * (1.0e6*p_hcd_beam_injected_total_mw)**exprf
# #327
self.data.costs.c2233 = (
1.0e-6
* self.data.costs.ucnbi
* (1.0e6 * self.data.current_drive.p_beam_injected_mw) ** exprf
)
if self.data.costs.ifueltyp == 1:
self.data.costs.c2233 = (
1.0e0 - self.data.costs.fcdfuel
) * self.data.costs.c2233
self.data.costs.c2233 = self.data.costs.fkind * self.data.costs.c2233
else:
# IFE driver costs (depends on driver type)
# Assume offset linear form for generic and SOMBRERO types,
# or one of two offset linear forms for OSIRIS type
if self.data.ife.ifedrv == 2:
if self.data.ife.dcdrv1 <= self.data.ife.dcdrv2:
switch = 0.0e0
else:
switch = (self.data.ife.cdriv2 - self.data.ife.cdriv1) / (
self.data.ife.dcdrv1 - self.data.ife.dcdrv2
)
if self.data.ife.edrive <= switch:
self.data.costs.c2231 = self.data.ife.mcdriv * (
self.data.ife.cdriv1
+ self.data.ife.dcdrv1 * 1.0e-6 * self.data.ife.edrive
)
else:
self.data.costs.c2231 = self.data.ife.mcdriv * (
self.data.ife.cdriv2
+ self.data.ife.dcdrv2 * 1.0e-6 * self.data.ife.edrive
)
elif self.data.ife.ifedrv == 3:
self.data.costs.c2231 = (
self.data.ife.mcdriv
* 1.0e-6
* self.data.ife.cdriv3
* (self.data.ife.edrive / self.data.ife.etadrv)
)
else:
self.data.costs.c2231 = self.data.ife.mcdriv * (
self.data.ife.cdriv0
+ self.data.ife.dcdrv0 * 1.0e-6 * self.data.ife.edrive
)
if self.data.costs.ifueltyp == 1:
self.data.costs.c2231 = (
1.0e0 - self.data.costs.fcdfuel
) * self.data.costs.c2231
self.data.costs.c2231 = self.data.costs.fkind * self.data.costs.c2231
self.data.costs.c2232 = 0.0e0
self.data.costs.c2233 = 0.0e0
self.data.costs.c2234 = 0.0e0
# Total account 223
self.data.costs.c223 = (
self.data.costs.c2231
+ self.data.costs.c2232
+ self.data.costs.c2233
+ self.data.costs.c2234
)
self.data.costs.cdcost = self.data.costs.c223
def acc224(self):
"""Account 224 : Vacuum system
This routine evaluates the Account 224 (vacuum system) costs.
The costs are scaled from TETRA reactor code runs.
"""
if (
VacuumPumpType(self.data.vacuum.i_vacuum_pump_type)
== VacuumPumpType.COMPOUND_CRYOPUMP
):
self.data.costs.c2241 = (
1.0e-6 * self.data.vacuum.n_vac_pumps_high * self.data.costs.UCCPMP
)
else:
self.data.costs.c2241 = (
1.0e-6 * self.data.vacuum.n_vac_pumps_high * self.data.costs.UCTPMP
)
self.data.costs.c2241 = self.data.costs.fkind * self.data.costs.c2241
# Account 224.2 : Backing pumps
self.data.costs.c2242 = (
1.0e-6 * self.data.vacuum.n_vv_vacuum_ducts * self.data.costs.UCBPMP
)
self.data.costs.c2242 = self.data.costs.fkind * self.data.costs.c2242
# Account 224.3 : Vacuum duct
self.data.costs.c2243 = (
1.0e-6
* self.data.vacuum.n_vv_vacuum_ducts
* self.data.vacuum.dlscal
* self.data.costs.UCDUCT
)
self.data.costs.c2243 = self.data.costs.fkind * self.data.costs.c2243
# Account 224.4 : Valves
self.data.costs.c2244 = (
1.0e-6
* 2.0e0
* self.data.vacuum.n_vv_vacuum_ducts
* (self.data.vacuum.dia_vv_vacuum_ducts * 1.2e0) ** 1.4e0
* self.data.costs.UCVALV
)
self.data.costs.c2244 = self.data.costs.fkind * self.data.costs.c2244
# Account 224.5 : Duct shielding
self.data.costs.c2245 = (
1.0e-6
* self.data.vacuum.n_vv_vacuum_ducts
* self.data.vacuum.m_vv_vacuum_duct_shield
* self.data.costs.UCVDSH
)
self.data.costs.c2245 = self.data.costs.fkind * self.data.costs.c2245
# Account 224.6 : Instrumentation
self.data.costs.c2246 = 1.0e-6 * self.data.costs.UCVIAC
self.data.costs.c2246 = self.data.costs.fkind * self.data.costs.c2246
# Total account 224
self.data.costs.c224 = (
self.data.costs.c2241
+ self.data.costs.c2242
+ self.data.costs.c2243
+ self.data.costs.c2244
+ self.data.costs.c2245
+ self.data.costs.c2246
)
def acc2251(self):
"""Account 225.1 : TF coil power conditioning
This routine evaluates the Account 225.1 (TF coil power
conditioning) costs.
Costs are developed based on the major equipment specification
of the tfcpwr module. A multiplier is used to account for bulk
materials and installation.
"""
expel = 0.7e0
self.data.costs.c22511 = (
1.0e-6
* self.data.costs.uctfps
* (self.data.tfcoil.tfckw * 1.0e3 + self.data.tfcoil.tfcmw * 1.0e6) ** expel
)
self.data.costs.c22511 = self.data.costs.fkind * self.data.costs.c22511
# Account 225.1.2 : TF coil breakers (zero cost for copper coils)
if self.data.tfcoil.i_tf_sup == TFConductorModel.SUPERCONDUCTING:
self.data.costs.c22512 = 1.0e-6 * (
self.data.costs.uctfbr
* self.data.tfcoil.n_tf_coils
* (
self.data.tfcoil.c_tf_turn
* self.data.tfcoil.v_tf_coil_dump_quench_kv
* 1.0e3
)
** expel
+ self.data.costs.uctfsw * self.data.tfcoil.c_tf_turn
)
else:
self.data.costs.c22512 = 0.0e0
self.data.costs.c22512 = self.data.costs.fkind * self.data.costs.c22512
# Account 225.1.3 : TF coil dump resistors
self.data.costs.c22513 = 1.0e-6 * (
1.0e9
* self.data.costs.UCTFDR
* self.data.tfcoil.e_tf_magnetic_stored_total_gj
+ self.data.costs.UCTFGR * 0.5e0 * self.data.tfcoil.n_tf_coils
)
self.data.costs.c22513 = self.data.costs.fkind * self.data.costs.c22513
# Account 225.1.4 : TF coil instrumentation and control
self.data.costs.c22514 = (
1.0e-6 * self.data.costs.UCTFIC * (30.0e0 * self.data.tfcoil.n_tf_coils)
)
self.data.costs.c22514 = self.data.costs.fkind * self.data.costs.c22514
# Account 225.1.5 : TF coil bussing
if self.data.tfcoil.i_tf_sup != TFConductorModel.SUPERCONDUCTING:
self.data.costs.c22515 = (
1.0e-6 * self.data.costs.uctfbus * self.data.tfcoil.m_tf_bus
)
else:
self.data.costs.c22515 = (
1.0e-6
* self.data.costs.ucbus
* self.data.tfcoil.c_tf_turn
* self.data.tfcoil.len_tf_bus
)
self.data.costs.c22515 = self.data.costs.fkind * self.data.costs.c22515
# Total account 225.1
self.data.costs.c2251 = (
self.data.costs.c22511
+ self.data.costs.c22512
+ self.data.costs.c22513
+ self.data.costs.c22514
+ self.data.costs.c22515
)
def acc2252(self):
"""Account 225.2 : PF coil power conditioning
This routine evaluates the Account 225.2 (PF coil power
conditioning) costs.
Costs are taken from the equipment specification of the
<A HREF="pfpwr.html">pfpwr</A> routine from the plant power module.
"""
self.data.costs.c22521 = (
1.0e-6 * self.data.costs.ucpfps * self.data.heat_transport.peakmva
)
self.data.costs.c22521 = self.data.costs.fkind * self.data.costs.c22521
# Account 225.2.2 : PF coil instrumentation and control
self.data.costs.c22522 = (
1.0e-6 * self.data.costs.ucpfic * self.data.pf_power.pfckts * 30.0e0
)
self.data.costs.c22522 = self.data.costs.fkind * self.data.costs.c22522
# Account 225.2.3 : PF coil bussing
self.data.costs.c22523 = (
1.0e-6
* self.data.costs.ucpfb
* self.data.pf_power.spfbusl
* self.data.pf_power.acptmax
)
self.data.costs.c22523 = self.data.costs.fkind * self.data.costs.c22523
# Account 225.2.4 : PF coil burn power supplies
if self.data.pf_power.pfckts != 0.0e0: # noqa: RUF069
self.data.costs.c22524 = (
1.0e-6
* self.data.costs.ucpfbs
* self.data.pf_power.pfckts
* (self.data.pf_power.srcktpm / self.data.pf_power.pfckts) ** 0.7e0
)
else:
self.data.costs.c22524 = 0.0e0
self.data.costs.c22524 = self.data.costs.fkind * self.data.costs.c22524
# Account 225.2.5 : PF coil breakers
self.data.costs.c22525 = (
1.0e-6
* self.data.costs.ucpfbk
* self.data.pf_power.pfckts
* (self.data.pf_power.acptmax * self.data.pf_power.vpfskv) ** 0.7e0
)
self.data.costs.c22525 = self.data.costs.fkind * self.data.costs.c22525
# Account 225.2.6 : PF coil dump resistors
self.data.costs.c22526 = (
1.0e-6 * self.data.costs.ucpfdr1 * self.data.pf_power.ensxpfm
)
self.data.costs.c22526 = self.data.costs.fkind * self.data.costs.c22526
# Account 225.2.7 : PF coil AC breakers
self.data.costs.c22527 = (
1.0e-6 * self.data.costs.ucpfcb * self.data.pf_power.pfckts
)
self.data.costs.c22527 = self.data.costs.fkind * self.data.costs.c22527
# Total account 225.2
self.data.costs.c2252 = (
self.data.costs.c22521
+ self.data.costs.c22522
+ self.data.costs.c22523
+ self.data.costs.c22524
+ self.data.costs.c22525
+ self.data.costs.c22526
+ self.data.costs.c22527
)
def acc226(self):
"""Account 226 : Heat transport system
This routine evaluates the Account 226 (heat transport system) costs.
Costs are estimated from major equipment and heat transport
system loops developed in the heatpwr module of the code.
"""
self.data.costs.c226 = (
self.data.costs.c2261 + self.data.costs.c2262 + self.data.costs.c2263
)
def acc2261(self):
"""Account 2261 : Reactor cooling system
This routine evaluates the Account 2261 -
"""
cmlsa = [0.4000e0, 0.7000e0, 0.8500e0, 1.0000e0]
exphts = 0.7e0
# Pumps and piping system
# N.B. with blktmodel > 0, the blanket is assumed to be helium-cooled,
# but the shield etc. is water-cooled (i_blkt_coolant_type=2).
# Therefore, a slight inconsistency exists here...
self.data.costs.cpp = (
1.0e-6
* self.data.costs.uchts[self.data.fwbs.i_blkt_coolant_type - 1]
* (
(1.0e6 * self.data.heat_transport.p_fw_div_heat_deposited_mw) ** exphts
+ (1.0e6 * self.data.fwbs.p_blkt_nuclear_heat_total_mw) ** exphts
+ (1.0e6 * self.data.fwbs.p_shld_nuclear_heat_mw) ** exphts
)
)
self.data.costs.cpp = (
self.data.costs.fkind * self.data.costs.cpp * cmlsa[self.data.costs.lsa - 1]
)
# Primary heat exchangers
self.data.costs.chx = (
1.0e-6
* self.data.costs.UCPHX
* self.data.heat_transport.n_primary_heat_exchangers
* (
1.0e6
* self.data.heat_transport.p_plant_primary_heat_mw
/ self.data.heat_transport.n_primary_heat_exchangers
)
** exphts
)
self.data.costs.chx = (
self.data.costs.fkind * self.data.costs.chx * cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2261 = self.data.costs.chx + self.data.costs.cpp
def acc2262(self):
"""Account 2262 : Auxiliary component cooling
This routine evaluates the Account 2262 - Auxiliary component cooling
"""
cmlsa = 0.4000e0, 0.7000e0, 0.8500e0, 1.0000e0
exphts = 0.7e0
# Pumps and piping system
self.data.costs.cppa = (
1.0e-6
* self.data.costs.UCAHTS
* (
(1.0e6 * self.data.heat_transport.p_hcd_electric_loss_mw) ** exphts
+ (1.0e6 * self.data.heat_transport.p_cryo_plant_electric_mw) ** exphts
+ (1.0e6 * self.data.heat_transport.vachtmw) ** exphts
+ (1.0e6 * self.data.heat_transport.p_tritium_plant_electric_mw)
** exphts
+ (1.0e6 * self.data.heat_transport.fachtmw) ** exphts
)
)
if self.data.ife.ife == 1:
self.data.costs.cppa += (
1.0e-6
* self.data.costs.UCAHTS
* (
(1.0e6 * self.data.ife.tdspmw) ** exphts
+ (1.0e6 * self.data.ife.tfacmw) ** exphts
)
)
# Apply Nth kind and safety assurance factors
self.data.costs.cppa = (
self.data.costs.fkind * self.data.costs.cppa * cmlsa[self.data.costs.lsa - 1]
)
self.data.costs.c2262 = self.data.costs.cppa
def acc2263(self):
"""Account 2263 : Cryogenic system
This routine evaluates the Account 2263 - Cryogenic system
"""
cmlsa = 0.4000e0, 0.7000e0, 0.8500e0, 1.0000e0
expcry = 0.67e0
self.data.costs.c2263 = (
1.0e-6
* self.data.costs.uccry
* 4.5e0
/ self.data.tfcoil.temp_tf_cryo
* self.data.heat_transport.helpow**expcry
)
# Apply Nth kind and safety factors
self.data.costs.c2263 = (
self.data.costs.fkind
* self.data.costs.c2263
* cmlsa[self.data.costs.lsa - 1]
)
def acc227(self):
"""Account 227 : Fuel handling
This routine evaluates the Account 227 (fuel handling) costs.
Costs are scaled from TETRA reactor code runs.
"""
self.data.costs.c227 = (
self.data.costs.c2271
+ self.data.costs.c2272
+ self.data.costs.c2273
+ self.data.costs.c2274
)
def acc2271(self):
"""Account 2271 : Fuelling system
This routine evaluates the Account 2271 - Fuelling system
"""
self.data.costs.c2271 = 1.0e-6 * self.data.costs.ucf1
# Apply Nth kind factor
self.data.costs.c2271 = self.data.costs.fkind * self.data.costs.c2271
def acc2272(self):
"""Account 2272 : Fuel processing and purification
This routine evaluates the Account 2272 - Fuel processing
"""
if self.data.ife.ife != 1:
# Previous calculation, using molflow_plasma_fuelling_required in Amps:
# 1.3 should have been
# self.data.physics.m_fuel_amu*umass/electron_charge*1000*s/day = 2.2
# wtgpd = burnup * molflow_plasma_fuelling_required * 1.3e0
# New calculation: 2 nuclei * reactions/sec * kg/nucleus * g/kg * sec/day
self.data.physics.wtgpd = (
2.0e0
* self.data.physics.rndfuel
* self.data.physics.m_fuel_amu
* constants.UMASS
* 1000.0e0
* 86400.0e0
)
else:
targtm = (
self.data.ife.gain
* self.data.ife.edrive
* 3.0e0
* 1.67e-27
* 1.0e3
/ (constants.ELECTRON_VOLT * 17.6e6 * self.data.ife.fburn)
)
self.data.physics.wtgpd = targtm * self.data.ife.reprat * 86400.0e0
# Assumes that He3 costs same as tritium to process...
self.data.costs.c2272 = (
1.0e-6
* self.data.costs.UCFPR
* (0.5e0 + 0.5e0 * (self.data.physics.wtgpd / 60.0e0) ** 0.67e0)
)
self.data.costs.c2272 = self.data.costs.fkind * self.data.costs.c2272
def acc2273(self):
"""Account 2273 : Atmospheric recovery systems
This routine evaluates the Account 2273 - Atmospheric recovery systems
"""
cfrht = 1.0e5
# No detritiation needed if purely D-He3 reaction
if self.data.physics.f_plasma_fuel_tritium > 1.0e-3:
self.data.costs.c2273 = (
1.0e-6
* self.data.costs.UCDTC
* (
(cfrht / 1.0e4) ** 0.6e0
* (self.data.buildings.volrci + self.data.buildings.wsvol)
)
)
else:
self.data.costs.c2273 = 0.0e0
self.data.costs.c2273 = self.data.costs.fkind * self.data.costs.c2273
def acc2274(self):
"""Account 2274 : Nuclear building ventilation
This routine evaluates the Account 2274 - Nuclear building ventilation
"""
self.data.costs.c2274 = (
1.0e-6
* self.data.costs.UCNBV
* (self.data.buildings.volrci + self.data.buildings.wsvol) ** 0.8e0
)
# Apply Nth kind factor
self.data.costs.c2274 = self.data.costs.fkind * self.data.costs.c2274
def acc228(self):
"""Account 228 : Instrumentation and control
This routine evaluates the Account 228 (instrumentation and
control) costs.
Costs are based on TFCX and INTOR.
"""
self.data.costs.c228 = 1.0e-6 * self.data.costs.uciac
self.data.costs.c228 = self.data.costs.fkind * self.data.costs.c228
def acc229(self):
"""Account 229 : Maintenance equipment
This routine evaluates the Account 229 (maintenance equipment) costs.
"""
self.data.costs.c229 = 1.0e-6 * self.data.costs.ucme
self.data.costs.c229 = self.data.costs.fkind * self.data.costs.c229
def acc23(self):
"""Account 23 : Turbine plant equipment
This routine evaluates the Account 23 (turbine plant equipment) costs.
"""
exptpe = 0.83e0
if self.data.costs.ireactor == 1:
self.data.costs.c23 = (
1.0e-6
* self.data.costs.ucturb[self.data.fwbs.i_blkt_coolant_type - 1]
* (self.data.heat_transport.p_plant_electric_gross_mw / 1200.0e0)
** exptpe
)
def acc24(self):
"""Account 24 : Electric plant equipment
This routine evaluates the Account 24 (electric plant equipment) costs.
"""
self.data.costs.c24 = (
self.data.costs.c241
+ self.data.costs.c242
+ self.data.costs.c243
+ self.data.costs.c244
+ self.data.costs.c245
)
def acc241(self):
"""Account 241 : Electric plant equipment - switchyard
This routine evaluates the Account 241 - switchyard
"""
cmlsa = 0.5700e0, 0.7850e0, 0.8925e0, 1.0000e0
# Account 241 : Switchyard
self.data.costs.c241 = (
1.0e-6 * self.data.costs.UCSWYD * cmlsa[self.data.costs.lsa - 1]
)
def acc242(self):
"""Account 242 : Electric plant equipment - Transformers
This routine evaluates the Account 242 - Transformers
"""
cmlsa = 0.5700e0, 0.7850e0, 0.8925e0, 1.0000e0
expepe = 0.9e0
# Account 242 : Transformers
self.data.costs.c242 = 1.0e-6 * (
self.data.costs.UCPP * (self.data.heat_transport.pacpmw * 1.0e3) ** expepe
+ self.data.costs.UCAP
* (self.data.heat_transport.p_plant_electric_base_total_mw * 1.0e3)
)
# Apply safety assurance factor
self.data.costs.c242 *= cmlsa[self.data.costs.lsa - 1]
def acc243(self):
"""Account 243 : Electric plant equipment - Low voltage
This routine evaluates the Account 243 - Low voltage
"""
cmlsa = 0.5700e0, 0.7850e0, 0.8925e0, 1.0000e0
# Account 243 : Low voltage
# (include 0.8 factor for transformer efficiency)
self.data.costs.c243 = (
1.0e-6
* self.data.costs.UCLV
* self.data.heat_transport.tlvpmw
* 1.0e3
/ 0.8e0
* cmlsa[self.data.costs.lsa - 1]
)
def acc244(self):
"""Account 244 : Electric plant equipment - Diesel generators
This routine evaluates the Account 244 - Diesel generators
"""
cmlsa = [0.5700e0, 0.7850e0, 0.8925e0, 1.0000e0]
# Account 244 : Diesel generator (8 MW per generator, assume 4 )
self.data.costs.c244 = (
1.0e-6 * self.data.costs.UCDGEN * 4.0e0 * cmlsa[self.data.costs.lsa - 1]
)
def acc245(self):
"""Account 245 : Electric plant equipment - Aux facility power
This routine evaluates the Account 245 - Aux facility power
"""
cmlsa = 0.5700e0, 0.7850e0, 0.8925e0, 1.0000e0
# Account 245 : Auxiliary facility power needs
self.data.costs.c245 = (
1.0e-6 * self.data.costs.UCAF * cmlsa[self.data.costs.lsa - 1]
)
def acc25(self):
"""Account 25 : Miscellaneous plant equipment
This routine evaluates the Account 25 (miscellaneous plant
equipment) costs, such as waste treatment.
"""
cmlsa = 0.7700e0, 0.8850e0, 0.9425e0, 1.0000e0
self.data.costs.c25 = (
1.0e-6 * self.data.costs.ucmisc * cmlsa[self.data.costs.lsa - 1]
)
def acc26(self):
"""Account 26 : Heat rejection system
This routine evaluates the Account 26 (heat rejection system) costs.
Costs are scaled with the total plant heat rejection based on
commercial systems.
J. Delene, private communication, ORNL, June 1990
"""
cmlsa = [0.8000e0, 0.9000e0, 0.9500e0, 1.0000e0]
# Calculate rejected heat for non-reactor (==0) and reactor (==1)
if self.data.costs.ireactor == 0:
pwrrej = (
self.data.physics.p_fusion_total_mw
+ self.data.heat_transport.p_hcd_electric_total_mw
+ self.data.tfcoil.tfcmw
)
else:
pwrrej = (
self.data.heat_transport.p_plant_primary_heat_mw
- self.data.heat_transport.p_plant_electric_gross_mw
)
# self.data.costs.uchrs - reference cost of heat rejection system [$]
self.data.costs.c26 = (
1.0e-6
* self.data.costs.uchrs
* pwrrej
/ 2300.0e0
* cmlsa[self.data.costs.lsa - 1]
)
def acc9(self):
"""Account 9 : Indirect cost and contingency allowances
This routine evaluates the Account 9 (indirect cost and
contingency allowances) costs.
The cost modelling is based on the commercial plant model of a
single contractor performing all plant engineering and construction
management, using commercially purchased equipment and materials.
<P>The project contingency is an allowance for incomplete design
specification and unforeseen events during the plant construction.
<P>The factors used are estimated from commercial plant experience.
J. Delene, private communication, ORNL, June 1990
"""
self.data.costs.cindrt = (
self.data.costs.cfind[self.data.costs.lsa - 1]
* self.data.costs.cdirt
* (1.0e0 + self.data.costs.cowner)
)
# Contingency costs
self.data.costs.ccont = self.data.costs.fcontng * (
self.data.costs.cdirt + self.data.costs.cindrt
)
def acc2253(self):
"""Account 225.3 : Energy storage
This routine evaluates the Account 225.3 (energy storage) costs.
Raises
------
ProcessValueError
If illegal value used for istore",
"""
self.data.costs.c2253 = 0.0e0
# Thermal storage options for a pulsed reactor
# See F/MPE/MOD/CAG/PROCESS/PULSE/0008 and 0014
if self.data.pulse.i_pulsed_plant == 1:
if self.data.pulse.istore == 1:
# Option 1 from ELECTROWATT report
# Pulsed Fusion Reactor Study : AEA FUS 205
# Increased condensate tank capacity
self.data.costs.c2253 = 0.1e0
# Additional electrically-driven feedpump (50 per cent duty)
self.data.costs.c2253 += 0.8e0
# Increased turbine-generator duty (5 per cent duty)
self.data.costs.c2253 += 4.0e0
# Additional auxiliary transformer capacity and ancillaries
self.data.costs.c2253 += 0.5e0
# Increased drum capacity
self.data.costs.c2253 += 2.8e0
# Externally fired superheater
self.data.costs.c2253 += 29.0e0
elif self.data.pulse.istore == 2:
# Option 2 from ELECTROWATT report
# Pulsed Fusion Reactor Study : AEA FUS 205
# Increased condensate tank capacity
self.data.costs.c2253 = 0.1e0
# Additional electrically-driven feedpump (50 per cent duty)
self.data.costs.c2253 += 0.8e0
# Increased drum capacity
self.data.costs.c2253 += 2.8e0
# Increased turbine-generator duty (5 per cent duty)
self.data.costs.c2253 += 4.0e0
# Additional fired boiler (1 x 100 per cent duty)
self.data.costs.c2253 += 330.0e0
# HP/LP steam bypass system for auxiliary boiler
# (30 per cent boiler capacity)
self.data.costs.c2253 += 1.0e0
# Dump condenser
self.data.costs.c2253 += 2.0e0
# Increased cooling water system capacity
self.data.costs.c2253 += 18.0e0
elif self.data.pulse.istore == 3:
# Simplistic approach that assumes that a large stainless steel
# block acts as the thermal storage medium. No account is taken
# of the cost of the piping within the block, etc.
#
# shcss is the specific heat capacity of stainless steel (J/kg/K)
# self.data.pulse.dtstor is the maximum allowable temperature change in
# the stainless steel block (input)
shcss = 520.0e0
self.data.costs.c2253 = (
self.data.costs.ucblss
* (self.data.heat_transport.p_plant_primary_heat_mw * 1.0e6)
* self.data.times.t_plant_pulse_no_burn
/ (shcss * self.data.pulse.dtstor)
)
else:
raise ProcessValueError(
"Illegal value for istore", istore=self.data.pulse.istore
)
if self.data.pulse.istore < 3:
# Scale self.data.costs.c2253 with net electric power
self.data.costs.c2253 = (
self.data.costs.c2253
* self.data.heat_transport.p_plant_electric_net_mw
/ 1200.0e0
)
# It is necessary to convert from 1992 pounds to 1990 dollars
# Reasonable guess for the exchange rate + inflation factor
# inflation = 5% per annum; exchange rate = 1.5 dollars per pound
self.data.costs.c2253 *= 1.36e0
self.data.costs.c2253 = self.data.costs.fkind * self.data.costs.c2253
def coelc(self):
"""Routine to calculate the cost of electricity for a fusion power plant
outfile : input integer : output file unit
This routine performs the calculation of the cost of electricity
for a fusion power plant.
<P>Annual costs are in megadollars/year, electricity costs are in
millidollars/kWh, while other costs are in megadollars.
All values are based on 1990 dollars.
"""
if self.data.ife.ife == 1:
kwhpy = (
1.0e3
* self.data.heat_transport.p_plant_electric_net_mw
* (24.0e0 * constants.N_DAY_YEAR)
* self.data.costs.f_t_plant_available
)
else:
kwhpy = (
1.0e3
* self.data.heat_transport.p_plant_electric_net_mw
* (24.0e0 * constants.N_DAY_YEAR)
* self.data.costs.f_t_plant_available
* self.data.times.t_plant_pulse_burn
/ self.data.times.t_plant_pulse_total
)
# Costs due to reactor plant
# ==========================
# Interest on construction costs
self.data.costs.moneyint = self.data.costs.concost * (
self.data.costs.fcap0 - 1.0e0
)
# Capital costs
self.data.costs.capcost = self.data.costs.concost + self.data.costs.moneyint
# Annual cost of plant capital cost
anncap = self.data.costs.capcost * self.data.costs.fcr0
# SJP Issue #836
# Check for the condition when kwhpy=0
kwhpy = max(kwhpy, 1.0e-10)
# Cost of electricity due to plant capital cost
self.data.costs.coecap = 1.0e9 * anncap / kwhpy
# Costs due to first wall and blanket renewal
# ===========================================
# Compound interest factor
feffwbl = (1.0e0 + self.data.costs.discount_rate) ** self.data.fwbs.life_blkt
# Capital recovery factor
crffwbl = (feffwbl * self.data.costs.discount_rate) / (feffwbl - 1.0e0)
# Annual cost of replacements
annfwbl = (
(self.data.costs.fwallcst + self.data.costs.blkcst)
* (1.0e0 + self.data.costs.cfind[self.data.costs.lsa - 1])
* self.data.costs.fcap0cp
* crffwbl
)
if self.data.costs.ifueltyp == 2:
annfwbl *= 1.0e0 - self.data.fwbs.life_blkt_fpy / self.data.costs.life_plant
# Cost of electricity due to first wall/blanket replacements
coefwbl = 1.0e9 * annfwbl / kwhpy
# Costs due to divertor renewal
# =============================
if self.data.ife.ife == 1:
anndiv = 0.0e0
coediv = 0.0e0
else:
# Compound interest factor
fefdiv = (1.0e0 + self.data.costs.discount_rate) ** self.data.costs.life_div
# Capital recovery factor
crfdiv = (fefdiv * self.data.costs.discount_rate) / (fefdiv - 1.0e0)
# Annual cost of replacements
anndiv = (
self.data.costs.divcst
* (1.0e0 + self.data.costs.cfind[self.data.costs.lsa - 1])
* self.data.costs.fcap0cp
* crfdiv
)
# Cost of electricity due to divertor replacements
if self.data.costs.ifueltyp == 2:
anndiv *= (
1.0e0 - self.data.costs.life_div_fpy / self.data.costs.life_plant
)
coediv = 1.0e9 * anndiv / kwhpy
# Costs due to centrepost renewal
# ===============================
if (self.data.physics.itart == 1) and (self.data.ife.ife != 1):
# Compound interest factor
fefcp = (1.0e0 + self.data.costs.discount_rate) ** self.data.costs.cplife_cal
# Capital recovery factor
crfcp = (fefcp * self.data.costs.discount_rate) / (fefcp - 1.0e0)
# Annual cost of replacements
anncp = (
self.data.costs.cpstcst
* (1.0e0 + self.data.costs.cfind[self.data.costs.lsa - 1])
* self.data.costs.fcap0cp
* crfcp
)
# Cost of electricity due to centrepost replacements
if self.data.costs.ifueltyp == 2:
anncp *= 1.0e0 - self.data.costs.cplife / self.data.costs.life_plant
coecp = 1.0e9 * anncp / kwhpy
else:
anncp = 0.0e0
coecp = 0.0e0
# Costs due to partial current drive system renewal
# =================================================
# Compound interest factor
fefcdr = (1.0e0 + self.data.costs.discount_rate) ** self.data.costs.cdrlife_cal
# Capital recovery factor
crfcdr = (fefcdr * self.data.costs.discount_rate) / (fefcdr - 1.0e0)
# Annual cost of replacements
if self.data.costs.ifueltyp == 0:
anncdr = 0.0e0
else:
anncdr = (
self.data.costs.cdcost
* self.data.costs.fcdfuel
/ (1.0e0 - self.data.costs.fcdfuel)
* (1.0e0 + self.data.costs.cfind[self.data.costs.lsa - 1])
* self.data.costs.fcap0cp
* crfcdr
)
# Cost of electricity due to current drive system replacements
coecdr = 1.0e9 * anncdr / kwhpy
# Costs due to operation and maintenance
# ======================================
# Annual cost of operation and maintenance
if self.data.heat_transport.p_plant_electric_net_mw < 0:
sqrt_p_plant_electric_net_mw_1200 = 0.0
logger.warning(
"p_plant_electric_net_mw has gone negative! "
"Clamping it to 0 for the calculation of annoam and annwst "
"(cost of maintenance and cost of waste)."
)
else:
sqrt_p_plant_electric_net_mw_1200 = np.sqrt(
self.data.heat_transport.p_plant_electric_net_mw / 1200.0e0
)
annoam = (
self.data.costs.ucoam[self.data.costs.lsa - 1]
* sqrt_p_plant_electric_net_mw_1200
)
# Cost of electricity due to operation and maintenance
self.data.costs.coeoam = 1.0e9 * annoam / kwhpy
# Costs due to reactor fuel
# =========================
# Annual cost of fuel
if self.data.ife.ife != 1:
# Sum D-T fuel cost and He3 fuel cost
annfuel = (
self.data.costs.ucfuel
* self.data.heat_transport.p_plant_electric_net_mw
/ 1200.0e0
+ 1.0e-6
* self.data.physics.f_plasma_fuel_helium3
* self.data.physics.wtgpd
* 1.0e-3
* self.data.costs.uche3
* constants.N_DAY_YEAR
* self.data.costs.f_t_plant_available
)
else:
annfuel = (
1.0e-6
* self.data.ife.uctarg
* self.data.ife.reprat
* 3.1536e7
* self.data.costs.f_t_plant_available
)
# Cost of electricity due to reactor fuel
coefuel = 1.0e9 * annfuel / kwhpy
# Costs due to waste disposal
# ===========================
# Annual cost of waste disposal
annwst = (
self.data.costs.ucwst[self.data.costs.lsa - 1]
* sqrt_p_plant_electric_net_mw_1200
)
# Cost of electricity due to waste disposal
coewst = 1.0e9 * annwst / kwhpy
# Costs due to decommissioning fund
# =================================
# Annual contributions to fund for decommissioning
# A fraction self.data.costs.decomf of the construction cost is set aside for
# this purpose at the start of the plant life.
# Final factor takes into account inflation over the plant lifetime
# (suggested by Tim Hender 07/03/96)
# Difference (self.data.costs.dintrt) between borrowing and
# saving interest rates is included,
# along with the possibility of completing the fund self.data.costs.dtlife
# years before the end of the plant's lifetime
anndecom = (
self.data.costs.decomf
* self.data.costs.concost
* self.data.costs.fcr0
/ (1.0e0 + self.data.costs.discount_rate - self.data.costs.dintrt)
** (self.data.costs.life_plant - self.data.costs.dtlife)
)
# Cost of electricity due to decommissioning fund
coedecom = 1.0e9 * anndecom / kwhpy
# Total costs
# ===========
# Annual costs due to 'fuel-like' components
# annfuelt = annfwbl + anndiv + anncdr + anncp + annfuel + annwst
# Total cost of electricity due to 'fuel-like' components
self.data.costs.coefuelt = coefwbl + coediv + coecdr + coecp + coefuel + coewst
# Total annual costs
# anntot = anncap + annfuelt + annoam + anndecom
# Total cost of electricity
self.data.costs.coe = (
self.data.costs.coecap
+ self.data.costs.coefuelt
+ self.data.costs.coeoam
+ coedecom
)
def convert_fpy_to_calendar(self):
"""Routine to convert component lifetimes in FPY to calendar years.
Required for replacement component costs.
"""
# FW/Blanket and HCD
if self.data.fwbs.life_blkt_fpy < self.data.costs.life_plant:
self.data.fwbs.life_blkt = (
self.data.fwbs.life_blkt_fpy * self.data.costs.f_t_plant_available
)
# Current drive system lifetime
# (assumed equal to first wall and blanket lifetime)
self.data.costs.cdrlife_cal = self.data.fwbs.life_blkt
else:
self.data.fwbs.life_blkt = self.data.fwbs.life_blkt_fpy
# Divertor
if self.data.costs.life_div_fpy < self.data.costs.life_plant:
self.data.costs.life_div = (
self.data.costs.life_div_fpy * self.data.costs.f_t_plant_available
)
else:
self.data.costs.life_div = self.data.costs.life_div_fpy
# Centrepost
if self.data.physics.itart == 1:
if self.data.costs.cplife < self.data.costs.life_plant:
self.data.costs.cplife_cal = (
self.data.costs.cplife * self.data.costs.f_t_plant_available
)
else:
self.data.costs.cplife_cal = self.data.costs.cplife
```
|