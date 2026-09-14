---
source: "https://ukaea.github.io/PROCESS/source/reference/process/data_structure/cost_variables/"
source_type: "url"
extracted_at: "2026-09-14T04:25:54.425430+00:00"
content_hash_sha256: "268c4874b958d5b0b8fdd3cde0d2b6f4bd8c29bb49ca2c807ebf3b2c0d5c3aed"
backend: "trafilatura"
title: "cost_variables"
---

# cost_variables


Module containing variables for the costs models

##
`CREATE_DICTS_FROM_DATACLASS = CostData`

`module-attribute`


##
`CostModels`


Bases: `IntEnum`


Enum for cost model selection

## Source code in `process/data_structure/cost_variables.py`


7 8 9 10 11 12 13 14 15 16 17 18 |
|

###
`PROCESS_1990 = 0`

`class-attribute`

`instance-attribute`


Use $ 1990 PROCESS model

###
`KOVARI_2014 = 1`

`class-attribute`

`instance-attribute`


Use $ 2014 Kovari model

###
`USER_PROVIDED = 2`

`class-attribute`

`instance-attribute`


Use user-provided model

##
`CostData`

`dataclass`


Dataclass holding cost variables

## Source code in `process/data_structure/cost_variables.py`


21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 121 122 123 124 125 126 127 128 129 130 131 132 133 134 135 136 137 138 139 140 141 142 143 144 145 146 147 148 149 150 151 152 153 154 155 156 157 158 159 160 161 162 163 164 165 166 167 168 169 170 171 172 173 174 175 176 177 178 179 180 181 182 183 184 185 186 187 188 189 190 191 192 193 194 195 196 197 198 199 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 218 219 220 221 222 223 224 225 226 227 228 229 230 231 232 233 234 235 236 237 238 239 240 241 242 243 244 245 246 247 248 249 250 251 252 253 254 255 256 257 258 259 260 261 262 263 264 265 266 267 268 269 270 271 272 273 274 275 276 277 278 279 280 281 282 283 284 285 286 287 288 289 290 291 292 293 294 295 296 297 298 299 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 318 319 320 321 322 323 324 325 326 327 328 329 330 331 332 333 334 335 336 337 338 339 340 341 342 343 344 345 346 347 348 349 350 351 352 353 354 355 356 357 358 359 360 361 362 363 364 365 366 367 368 369 370 371 372 373 374 375 376 377 378 379 380 381 382 383 384 385 386 387 388 389 390 391 392 393 394 395 396 397 398 399 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 418 419 420 421 422 423 424 425 426 427 428 429 430 431 432 433 434 435 436 437 438 439 440 441 442 443 444 445 446 447 448 449 450 451 452 453 454 455 456 457 458 459 460 461 462 463 464 465 466 467 468 469 470 471 472 473 474 475 476 477 478 479 480 481 482 483 484 485 486 487 488 489 490 491 492 493 494 495 496 497 498 499 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 518 519 520 521 522 523 524 525 526 527 528 529 530 531 532 533 534 535 536 537 538 539 540 541 542 543 544 545 546 547 548 549 550 551 552 553 554 555 556 557 558 559 560 561 562 563 564 565 566 567 568 569 570 571 572 573 574 575 576 577 578 579 580 581 582 583 584 585 586 587 588 589 590 591 592 593 594 595 596 597 598 599 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 618 619 620 621 622 623 624 625 626 627 628 629 630 631 632 633 634 635 636 637 638 639 640 641 642 643 644 645 646 647 648 649 650 651 652 653 654 655 656 657 658 659 660 661 662 663 664 665 666 667 668 669 670 671 672 673 674 675 676 677 678 679 680 681 682 683 684 685 686 687 688 689 690 691 692 693 694 695 696 697 698 699 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 718 719 720 721 722 723 724 725 726 727 728 729 730 731 732 733 734 735 736 737 738 739 740 741 742 743 744 745 746 747 748 749 750 751 752 753 754 755 756 757 758 759 760 761 762 763 764 765 766 767 768 769 770 771 772 773 774 775 776 777 778 779 780 781 782 783 784 785 786 787 788 789 790 791 792 793 794 795 796 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 818 819 820 821 822 823 824 825 826 827 828 829 830 831 832 833 834 |
|

###
`c228 = 0.0`

`class-attribute`

`instance-attribute`


c228 account cost

###
`c229 = 0.0`

`class-attribute`

`instance-attribute`


c229 account cost

###
`c23 = 0.0`

`class-attribute`

`instance-attribute`


c23 account cost

###
`c25 = 0.0`

`class-attribute`

`instance-attribute`


c25 account cost

###
`c26 = 0.0`

`class-attribute`

`instance-attribute`


c26 account cost

###
`cindrt = 0.0`

`class-attribute`

`instance-attribute`


cindrt account cost

###
`ccont = 0.0`

`class-attribute`

`instance-attribute`


ccont account cost

###
`c226 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2261 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2262 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2263 = 0.0`

`class-attribute`

`instance-attribute`


###
`c227 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2271 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2272 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2273 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2274 = 0.0`

`class-attribute`

`instance-attribute`


###
`c24 = 0.0`

`class-attribute`

`instance-attribute`


###
`c241 = 0.0`

`class-attribute`

`instance-attribute`


###
`c242 = 0.0`

`class-attribute`

`instance-attribute`


###
`c243 = 0.0`

`class-attribute`

`instance-attribute`


###
`c244 = 0.0`

`class-attribute`

`instance-attribute`


###
`c245 = 0.0`

`class-attribute`

`instance-attribute`


###
`c21 = 0.0`

`class-attribute`

`instance-attribute`


###
`c211 = 0.0`

`class-attribute`

`instance-attribute`


###
`c212 = 0.0`

`class-attribute`

`instance-attribute`


###
`c213 = 0.0`

`class-attribute`

`instance-attribute`


###
`c214 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2141 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2142 = 0.0`

`class-attribute`

`instance-attribute`


###
`c215 = 0.0`

`class-attribute`

`instance-attribute`


###
`c216 = 0.0`

`class-attribute`

`instance-attribute`


###
`c217 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2171 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2172 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2173 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2174 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2211 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2212 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22121 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22122 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22123 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22124 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22125 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22126 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22127 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2213 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22131 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22132 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2214 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2215 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2221 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22211 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22212 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22213 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22214 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22215 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2222 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22221 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22222 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22223 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22224 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2223 = 0.0`

`class-attribute`

`instance-attribute`


###
`c223 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2231 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2232 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2233 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2234 = 0.0`

`class-attribute`

`instance-attribute`


###
`c224 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2241 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2242 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2243 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2244 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2245 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2246 = 0.0`

`class-attribute`

`instance-attribute`


###
`c225 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2251 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22511 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22512 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22513 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22514 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22515 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2252 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22521 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22522 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22523 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22524 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22525 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22526 = 0.0`

`class-attribute`

`instance-attribute`


###
`c22527 = 0.0`

`class-attribute`

`instance-attribute`


###
`c2253 = 0.0`

`class-attribute`

`instance-attribute`


###
`chx = 0.0`

`class-attribute`

`instance-attribute`


###
`cpp = 0.0`

`class-attribute`

`instance-attribute`


###
`cppa = 0.0`

`class-attribute`

`instance-attribute`


###
`c22128 = 0.0`

`class-attribute`

`instance-attribute`


###
`abktflnc = 5.0`

`class-attribute`

`instance-attribute`


allowable first wall/blanket neutron fluence (MW-yr/m2) (`blktmodel=0`

)

###
`adivflnc = 7.0`

`class-attribute`

`instance-attribute`


allowable divertor heat fluence (MW-yr/m2)

###
`blkcst = 0.0`

`class-attribute`

`instance-attribute`


blanket direct cost (M$)

###
`c221 = 0.0`

`class-attribute`

`instance-attribute`


total account 221 cost (M$) - first wall, blanket, shield, support structure and div plates

###
`c222 = 0.0`

`class-attribute`

`instance-attribute`


total account 222 cost (M$) - TF coils + PF coils

###
`capcost = 0.0`

`class-attribute`

`instance-attribute`


total capital cost including interest (M$)

###
`cconfix = 80.0`

`class-attribute`

`instance-attribute`


fixed cost of superconducting cable ($/m)

###
`cconshpf = 70.0`

`class-attribute`

`instance-attribute`


cost of PF coil steel conduit/sheath ($/m)

###
`cconshtf = 75.0`

`class-attribute`

`instance-attribute`


cost of TF coil steel conduit/sheath ($/m)

###
`cdcost = 0.0`

`class-attribute`

`instance-attribute`


current drive direct costs (M$)

###
`cdirt = 0.0`

`class-attribute`

`instance-attribute`


total plant direct cost (M$)

###
`life_hcd_fpy = 0.0`

`class-attribute`

`instance-attribute`


Full power year lifetime of heating/current drive system (y)

###
`cdrlife_cal = 0.0`

`class-attribute`

`instance-attribute`


Calendar year lifetime of heating/current drive system (y)

###
`f_t_plant_available = 0.75`

`class-attribute`

`instance-attribute`


Total plant availability fraction; input if `i_plant_availability=0`


###
`cpfact = 0.0`

`class-attribute`

`instance-attribute`


Total plant capacity factor

###
`cfind = field(default_factory=lambda: [0.244, 0.244, 0.244, 0.29])`

`class-attribute`

`instance-attribute`


indirect cost factor (func of lsa) (cost model = 0)

###
`cland = 19.2`

`class-attribute`

`instance-attribute`


cost of land (M$)

###
`coe = 0.0`

`class-attribute`

`instance-attribute`


cost of electricity ($/MW-hr)

###
`coecap = 0.0`

`class-attribute`

`instance-attribute`


capital cost of electricity (m$/kW-hr)

###
`coefuelt = 0.0`

`class-attribute`

`instance-attribute`


'fuel' (including replaceable components) contribution to cost of electricity (m$/kW-hr)

###
`coeoam = 0.0`

`class-attribute`

`instance-attribute`


operation and maintenance contribution to cost of electricity (m$/kW-hr)

###
`concost = 0.0`

`class-attribute`

`instance-attribute`


plant construction cost (M$)

###
`costexp = 0.8`

`class-attribute`

`instance-attribute`


cost exponent for scaling in 2015 costs model

###
`costexp_pebbles = 0.6`

`class-attribute`

`instance-attribute`


cost exponent for pebbles in 2015 costs model

###
`cost_factor_buildings = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for buildings

###
`cost_factor_land = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for land

###
`cost_factor_tf_coils = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for TF coils

###
`cost_factor_fwbs = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for fwbs

###
`cost_factor_rh = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for remote handling

###
`cost_factor_vv = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for vacuum vessel

###
`cost_factor_bop = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for energy conversion system

###
`cost_factor_misc = 1.0`

`class-attribute`

`instance-attribute`


cost scaling factor for remaining subsystems

###
`maintenance_fwbs = 0.2`

`class-attribute`

`instance-attribute`


Maintenance cost factor: first wall, blanket, shield, divertor

###
`maintenance_gen = 0.05`

`class-attribute`

`instance-attribute`


Maintenance cost factor: All other components except coils, vacuum vessel, thermal shield, cryostat, land

###
`amortization = 13.6`

`class-attribute`

`instance-attribute`


amortization factor (fixed charge factor) "A" (years)

###
`i_cost_model = 1`

`class-attribute`

`instance-attribute`


Switch for cost model: - =0 use $ 1990 PROCESS model - =1 use $ 2014 Kovari model - =2 use user-provided model

###
`i_cp_lifetime = 0`

`class-attribute`

`instance-attribute`


Switch for the centrepost lifetime constraint 0 : The CP full power year lifetime is set by the user via cplife_input 1 : The CP lifetime is equal to the divertor lifetime 2 : The CP lifetime is equal to the breeding blankets lifetime 3 : The CP lifetime is equal to the plant lifetime

###
`cowner = 0.15`

`class-attribute`

`instance-attribute`


owner cost factor

###
`cplife_input = 2.0`

`class-attribute`

`instance-attribute`


User input full power year lifetime of the centrepost (years) (i_cp_lifetime = 0)

###
`cplife = 0.0`

`class-attribute`

`instance-attribute`


Calculated full power year lifetime of centrepost (years)

###
`cplife_cal = 0.0`

`class-attribute`

`instance-attribute`


Calculated calendar year lifetime of centrepost (years)

###
`cpstcst = 0.0`

`class-attribute`

`instance-attribute`


ST centrepost direct cost (M$)

###
`cpstflnc = 10.0`

`class-attribute`

`instance-attribute`


allowable ST centrepost neutron fluence (MW-yr/m2)

###
`crctcore = 0.0`

`class-attribute`

`instance-attribute`


reactor core costs (categories 221, 222 and 223)

###
`csi = 16.0`

`class-attribute`

`instance-attribute`


allowance for site costs (M$)

###
`cturbb = 38.0`

`class-attribute`

`instance-attribute`


cost of turbine building (M$)

###
`decomf = 0.1`

`class-attribute`

`instance-attribute`


proportion of constructed cost required for decommissioning fund

###
`dintrt = 0.0`

`class-attribute`

`instance-attribute`


diff between borrowing and saving interest rates

###
`divcst = 0.0`

`class-attribute`

`instance-attribute`


divertor direct cost (M$)

###
`life_div_fpy = 0.0`

`class-attribute`

`instance-attribute`


Full power year lifetime of divertor (fpy)

###
`life_div = 0.0`

`class-attribute`

`instance-attribute`


Calendar year lifetime of divertor (y)

###
`dtlife = 0.0`

`class-attribute`

`instance-attribute`


period prior to the end of the plant life that the decommissioning fund is used (years)

###
`fcap0 = 1.165`

`class-attribute`

`instance-attribute`


average cost of money for construction of plant assuming design/construction time of six years

###
`fcap0cp = 1.08`

`class-attribute`

`instance-attribute`


average cost of money for replaceable components assuming lead time for these of two years

###
`fcdfuel = 0.1`

`class-attribute`

`instance-attribute`


fraction of current drive cost treated as fuel (if `ifueltyp = 1`

)

###
`fcontng = 0.195`

`class-attribute`

`instance-attribute`


project contingency factor

###
`fcr0 = 0.0966`

`class-attribute`

`instance-attribute`


fixed charge rate during construction

###
`fkind = 1.0`

`class-attribute`

`instance-attribute`


multiplier for Nth of a kind costs

###
`fwallcst = 0.0`

`class-attribute`

`instance-attribute`


first wall cost (M$)

###
`i_plant_availability = 2`

`class-attribute`

`instance-attribute`


Switch for plant availability model: - =0 use input value for f_t_plant_available - =1 calculate f_t_plant_available using Taylor and Ward 1999 model - =2 calculate f_t_plant_available using new (2015) model - =3 calculate f_t_plant_available using ST model

###
`ibkt_life = 0`

`class-attribute`

`instance-attribute`


Switch for fw/blanket lifetime calculation in availability module: - =0 use neutron fluence model - =1 use fusion power model (DEMO only)

###
`life_dpa = 50`

`class-attribute`

`instance-attribute`


Allowable DPA from DEMO fw/blanket lifetime calculation in availability module

###
`bktcycles = 1000.0`

`class-attribute`

`instance-attribute`


Number of fusion cycles to reach allowable DPA from DEMO fw/blanket lifetime calculation

###
`f_t_plant_available_min = 0.75`

`class-attribute`

`instance-attribute`


Minimum allowed plant availability (`constraint equation 61`

)

###
`tok_build_cost_per_vol = 1283.0`

`class-attribute`

`instance-attribute`


Unit cost for tokamak complex buildings, including building and site services ($/m3)

###
`light_build_cost_per_vol = 270.0`

`class-attribute`

`instance-attribute`


Unit cost for unshielded non-active buildings ($/m3)

###
`num_rh_systems = 4`

`class-attribute`

`instance-attribute`


Number of remote handling systems (1-10)

###
`conf_mag = 0.99`

`class-attribute`

`instance-attribute`


c parameter, which determines the temperature margin at which magnet lifetime starts to decline

###
`div_prob_fail = 0.0002`

`class-attribute`

`instance-attribute`


Divertor probability of failure (per op day)

###
`div_umain_time = 0.25`

`class-attribute`

`instance-attribute`


Divertor unplanned maintenance time (years)

###
`div_nref = 7000.0`

`class-attribute`

`instance-attribute`


Reference value for cycle cycle life of divertor

###
`div_nu = 14000.0`

`class-attribute`

`instance-attribute`


The cycle when the divertor fails with 100% probability

###
`fwbs_nref = 20000.0`

`class-attribute`

`instance-attribute`


Reference value for cycle life of blanket

###
`fwbs_nu = 40000.0`

`class-attribute`

`instance-attribute`


The cycle when the blanket fails with 100% probability

###
`fwbs_prob_fail = 0.0002`

`class-attribute`

`instance-attribute`


Fwbs probability of failure (per op day)

###
`fwbs_umain_time = 0.25`

`class-attribute`

`instance-attribute`


Fwbs unplanned maintenance time (years)

###
`redun_vacp = 25.0`

`class-attribute`

`instance-attribute`


Vacuum system pump redundancy level (%)

###
`redun_vac = 0`

`class-attribute`

`instance-attribute`


Number of redundant vacuum pumps

###
`t_plant_operational_total_yrs = 0.0`

`class-attribute`

`instance-attribute`


Operational time (yrs)

###
`t_blkt_replace_yrs = 0.5`

`class-attribute`

`instance-attribute`


time taken to replace blanket (y) (`i_plant_availability=1`

)

###
`tcomrepl = 0.5`

`class-attribute`

`instance-attribute`


time taken to replace both blanket and divertor (y) (`i_plant_availability=1`

)

###
`t_div_replace_yrs = 0.25`

`class-attribute`

`instance-attribute`


Time taken to replace divertor (y) (`i_plant_availability=1`

)

###
`uubop = 0.02`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for balance of plant (`i_plant_availability=1`

)

###
`uucd = 0.02`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for current drive (`i_plant_availability=1`

)

###
`uudiv = 0.04`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for divertor (`i_plant_availability=1`

)

###
`uufuel = 0.02`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for fuel system (`i_plant_availability=1`

)

###
`uufw = 0.04`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for first wall (`i_plant_availability=1`

)

###
`uumag = 0.02`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for magnets (`i_plant_availability=1`

)

###
`uuves = 0.04`

`class-attribute`

`instance-attribute`


unplanned unavailability factor for vessel (`i_plant_availability=1`

)

###
`ifueltyp = 0`

`class-attribute`

`instance-attribute`


Switch for fuel type: - =2 treat initial blanket, divertor, first wall as capital costs. Treat all later items and fraction fcdfuel of CD equipment as fuel costs - =1 treat blanket divertor, first wall and fraction fcdfuel of CD equipment as fuel cost - =0 treat these as capital cost

###
`ipnet = 0`

`class-attribute`

`instance-attribute`


Switch for net electric power calculation: - =0 scale so that always > 0 - =1 let go < 0 (no c-o-e)

###
`ireactor = 1`

`class-attribute`

`instance-attribute`


Switch for net electric power and cost of electricity calculations: - =0 do not calculate MW(electric) or c-o-e - =1 calculate MW(electric) and c-o-e

###
`lsa = 4`

`class-attribute`

`instance-attribute`


Level of safety assurance switch (generally, use 3 or 4): - =1 truly passively safe plant - =2,3 in-between - =4 like current fission plant

###
`moneyint = 0.0`

`class-attribute`

`instance-attribute`


interest portion of capital cost (M$)

###
`output_costs = 1`

`class-attribute`

`instance-attribute`


Switch for costs output: - =0 do not write cost-related outputs to file - =1 write cost-related outputs to file

###
`discount_rate = 0.0435`

`class-attribute`

`instance-attribute`


effective cost of money in constant dollars

###
`startupratio = 1.0`

`class-attribute`

`instance-attribute`


ratio of additional HCD power for start-up to flat-top operational requirements

###
`startuppwr = 0.0`

`class-attribute`

`instance-attribute`


cost associated with additional HCD system power required on start-up ($)

###
`supercond_cost_model = 0`

`class-attribute`

`instance-attribute`


Switch for superconductor cost model: - =0 use $/kg - =1 use $/kAm

###
`life_plant = 30.0`

`class-attribute`

`instance-attribute`


Full power year plant lifetime (years)

###
`tmain = None`

`class-attribute`

`instance-attribute`


Maintenance time for replacing CP (years) (i_plant_availability = 3)

###
`u_unplanned_cp = 0.0`

`class-attribute`

`instance-attribute`


User-input CP unplanned unavailability (i_plant_availability = 3)

###
`UCAD = 180.0`

`class-attribute`

`instance-attribute`


unit cost for administration buildings (M$/m3)

###
`UCAF = 1500000.0`

`class-attribute`

`instance-attribute`


unit cost for aux facility power equipment ($)

###
`UCAHTS = 31.0`

`class-attribute`

`instance-attribute`


unit cost for aux heat transport equipment ($/W**exphts)

###
`UCAP = 17.0`

`class-attribute`

`instance-attribute`


unit cost of auxiliary transformer ($/kVA)

###
`ucblbe = 260.0`

`class-attribute`

`instance-attribute`


unit cost for blanket beryllium ($/kg)

###
`ucblbreed = 875.0`

`class-attribute`

`instance-attribute`


unit cost for breeder material ($/kg) (`blktmodel>0`

)

###
`ucblli = 875.0`

`class-attribute`

`instance-attribute`


unit cost for blanket lithium ($/kg) (30% Li6)

###
`ucblli2o = 600.0`

`class-attribute`

`instance-attribute`


unit cost for blanket Li_2O ($/kg)

###
`ucbllipb = 10.3`

`class-attribute`

`instance-attribute`


unit cost for blanket Li-Pb ($/kg) (30% Li6)

###
`ucblss = 90.0`

`class-attribute`

`instance-attribute`


unit cost for blanket stainless steel ($/kg)

###
`ucblvd = 200.0`

`class-attribute`

`instance-attribute`


unit cost for blanket vanadium ($/kg)

###
`UCBPMP = 292500.0`

`class-attribute`

`instance-attribute`


vacuum system backing pump cost ($)

###
`ucbus = 0.123`

`class-attribute`

`instance-attribute`


cost of aluminium bus for TF coil ($/A-m)

###
`uccase = 50.0`

`class-attribute`

`instance-attribute`


cost of superconductor case ($/kg)

###
`UCCO = 350.0`

`class-attribute`

`instance-attribute`


unit cost for control buildings (M$/m3)

###
`uccpcl1 = 250.0`

`class-attribute`

`instance-attribute`


cost of high strength tapered copper ($/kg)

###
`uccpclb = 150.0`

`class-attribute`

`instance-attribute`


cost of TF outboard leg plate coils ($/kg)

###
`UCCPMP = 390000.0`

`class-attribute`

`instance-attribute`


vacuum system cryopump cost ($)

###
`UCCR = 460.0`

`class-attribute`

`instance-attribute`


unit cost for cryogenic building (M$/vol)

###
`uccry = 93000.0`

`class-attribute`

`instance-attribute`


heat transport system cryoplant costs ($/W**expcry)

###
`uccryo = 32.0`

`class-attribute`

`instance-attribute`


unit cost for vacuum vessel ($/kg)

###
`uccu = 75.0`

`class-attribute`

`instance-attribute`


unit cost for copper in superconducting cable ($/kg)

###
`UCDGEN = 1700000.0`

`class-attribute`

`instance-attribute`


cost per 8 MW diesel generator ($)

###
`ucdiv = 280000.0`

`class-attribute`

`instance-attribute`


cost of divertor blade ($)

###
`UCDTC = 13.0`

`class-attribute`

`instance-attribute`


detritiation, air cleanup cost ($/10000m3/hr)

###
`UCDUCT = 42250.0`

`class-attribute`

`instance-attribute`


vacuum system duct cost ($/m)

###
`ucech = 3.0`

`class-attribute`

`instance-attribute`


ECH system cost ($/W)

###
`UCEL = 380.0`

`class-attribute`

`instance-attribute`


unit cost for electrical equipment building (M$/m3)

###
`UCES1 = 32000.0`

`class-attribute`

`instance-attribute`


MGF (motor-generator flywheel) cost factor ($/MVA**0.8)

###
`UCES2 = 8800.0`

`class-attribute`

`instance-attribute`


MGF (motor-generator flywheel) cost factor ($/MJ**0.8)

###
`ucf1 = 22300000.0`

`class-attribute`

`instance-attribute`


cost of fuelling system ($)

###
`ucfnc = 35.0`

`class-attribute`

`instance-attribute`


outer PF coil fence support cost ($/kg)

###
`UCFPR = 44000000.0`

`class-attribute`

`instance-attribute`


cost of 60g/day tritium processing unit ($)

###
`ucfuel = 3.45`

`class-attribute`

`instance-attribute`


unit cost of D-T fuel (M$/year/1200MW)

###
`UCFWA = 60000.0`

`class-attribute`

`instance-attribute`


first wall armour cost ($/m2)

###
`UCFWPS = 10000000.0`

`class-attribute`

`instance-attribute`


first wall passive stabiliser cost ($)

###
`UCFWS = 53000.0`

`class-attribute`

`instance-attribute`


first wall structure cost ($/m2)

###
`UCGSS = 35.0`

`class-attribute`

`instance-attribute`


cost of reactor structure ($/kg)

###
`uche3 = 1000000.0`

`class-attribute`

`instance-attribute`


cost of helium-3 ($/kg)

###
`uchrs = 87900000.0`

`class-attribute`

`instance-attribute`


cost of heat rejection system ($)

###
`uchts = field(default_factory=lambda: [15.3, 19.1])`

`class-attribute`

`instance-attribute`


cost of heat transport system equipment per loop ($/W); dependent on coolant type (i_blkt_coolant_type)

###
`uciac = 150000000.0`

`class-attribute`

`instance-attribute`


cost of instrumentation, control & diagnostics ($)

###
`ucich = 3.0`

`class-attribute`

`instance-attribute`


ICH system cost ($/W)

###
`UCINT = 35.0`

`class-attribute`

`instance-attribute`


superconductor intercoil structure cost ($/kg)

###
`uclh = 3.3`

`class-attribute`

`instance-attribute`


lower hybrid system cost ($/W)

###
`UCLV = 16.0`

`class-attribute`

`instance-attribute`


low voltage system cost ($/kVA)

###
`UCMB = 260.0`

`class-attribute`

`instance-attribute`


unit cost for reactor maintenance building (M$/m3)

###
`ucme = 125000000.0`

`class-attribute`

`instance-attribute`


cost of maintenance equipment ($)

###
`ucmisc = 25000000.0`

`class-attribute`

`instance-attribute`


miscellaneous plant allowance ($)

###
`ucnbi = 3.3`

`class-attribute`

`instance-attribute`


NBI system cost ($/W)

###
`UCNBV = 1000.0`

`class-attribute`

`instance-attribute`


cost of nuclear building ventilation ($/m3)

###
`ucoam = field(default_factory=lambda: [68.8, 68.8, 68.8, 74.4])`

`class-attribute`

`instance-attribute`


annual cost of operation and maintenance (M$/year/1200MW**0.5)

###
`ucpens = 32.0`

`class-attribute`

`instance-attribute`


penetration shield cost ($/kg)

###
`ucpfb = 210.0`

`class-attribute`

`instance-attribute`


cost of PF coil buses ($/kA-m)

###
`ucpfbk = 16600.0`

`class-attribute`

`instance-attribute`


cost of PF coil DC breakers ($/MVA**0.7)

###
`ucpfbs = 4900.0`

`class-attribute`

`instance-attribute`


cost of PF burn power supplies ($/kW**0.7)

###
`ucpfcb = 75000.0`

`class-attribute`

`instance-attribute`


cost of PF coil AC breakers ($/circuit)

###
`ucpfdr1 = 150.0`

`class-attribute`

`instance-attribute`


cost factor for dump resistors ($/MJ)

###
`ucpfic = 10000.0`

`class-attribute`

`instance-attribute`


cost of PF instrumentation and control ($/channel)

###
`ucpfps = 35000.0`

`class-attribute`

`instance-attribute`


cost of PF coil pulsed power supplies ($/MVA)

###
`UCPHX = 15.0`

`class-attribute`

`instance-attribute`


primary heat transport cost ($/W**exphts)

###
`UCPP = 48.0`

`class-attribute`

`instance-attribute`


cost of primary power transformers ($/kVA**0.9)

###
`ucrb = 400.0`

`class-attribute`

`instance-attribute`


cost of reactor building (M$/m3)

###
`ucsc = field(default_factory=lambda: [600.0, 600.0, 300.0, 600.0, 600.0, 600.0, 300.0, 1200.0, 1200.0])`

`class-attribute`

`instance-attribute`


cost of superconductor ($/kg)

###
`sc_mat_cost_0 = field(default_factory=lambda: [4.8, 2.0, 1.0, 4.8, 4.8, 47.4, 1.0, 47.4, 47.4])`

`class-attribute`

`instance-attribute`


cost of superconductor ($/kA m) at 6.4 T, 4.2 K

###
`UCSH = 115.0`

`class-attribute`

`instance-attribute`


cost of shops and warehouses (M$/m3)

###
`ucshld = 32.0`

`class-attribute`

`instance-attribute`


cost of shield structural steel ($/kg)

###
`UCSWYD = 18400000.0`

`class-attribute`

`instance-attribute`


switchyard equipment costs ($)

###
`uctfbr = 1.22`

`class-attribute`

`instance-attribute`


cost of TF coil breakers ($/W**0.7)

###
`uctfbus = 100.0`

`class-attribute`

`instance-attribute`


cost of TF coil bus ($/kg)

###
`UCTFDR = 0.000175`

`class-attribute`

`instance-attribute`


cost of TF coil dump resistors ($/J)

###
`UCTFGR = 5000.0`

`class-attribute`

`instance-attribute`


additional cost of TF coil dump resistors ($/coil)

###
`UCTFIC = 10000.0`

`class-attribute`

`instance-attribute`


cost of TF coil instrumentation and control ($/coil/30)

###
`uctfps = 24.0`

`class-attribute`

`instance-attribute`


cost of TF coil power supplies ($/W**0.7)

###
`uctfsw = 1.0`

`class-attribute`

`instance-attribute`


cost of TF coil slow dump switches ($/A)

###
`UCTPMP = 110500.0`

`class-attribute`

`instance-attribute`


cost of turbomolecular pump ($)

###
`UCTR = 370.0`

`class-attribute`

`instance-attribute`


cost of tritium building ($/m3)

###
`ucturb = field(default_factory=lambda: [230000000.0, 245000000.0])`

`class-attribute`

`instance-attribute`


cost of turbine plant equipment ($) (dependent on coolant type i_blkt_coolant_type)

###
`UCVALV = 390000.0`

`class-attribute`

`instance-attribute`


vacuum system valve cost ($)

###
`UCVDSH = 26.0`

`class-attribute`

`instance-attribute`


vacuum duct shield cost ($/kg)

###
`UCVIAC = 1300000.0`

`class-attribute`

`instance-attribute`


vacuum system instrumentation and control cost ($)

###
`ucwindpf = 465.0`

`class-attribute`

`instance-attribute`


cost of PF coil superconductor windings ($/m)

###
`ucwindtf = 480.0`

`class-attribute`

`instance-attribute`


cost of TF coil superconductor windings ($/m)

###
`UCWS = 460.0`

`class-attribute`

`instance-attribute`


cost of active assembly shop ($/m3)

###
`ucwst = field(default_factory=lambda: [0.0, 3.94, 5.91, 7.88])`

`class-attribute`

`instance-attribute`


cost of waste disposal (M$/y/1200MW)