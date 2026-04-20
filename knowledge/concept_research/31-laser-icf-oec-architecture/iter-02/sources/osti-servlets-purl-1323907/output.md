---
source: "https://www.osti.gov/servlets/purl/1323907"
source_type: "url"
extracted_at: "2026-04-20T18:24:46.980857+00:00"
content_hash_sha256: "4e28807aa93d9061a48c0e5fe5e10ca9915ffa5c02cd1776e581de07630ceee1"
backend: "pdf_pipeline"
---

**SANDIA REPORT** SAND2006-4147 Unlimited Release Printed December 2013 

Steven A. Wright, Milton E. Vernon, Paul S. Pickard 

Prepared by Sandia National Laboratories Albuquerque, New Mexico  87185 and Livermore, California  94550 

Sandia is a multiprogram laboratory operated by Sandia Corporation, a Lockheed Martin Company, for the United States Department of Energy’s National Nuclear Security Administration under Contract DE-AC04-94AL85000. 

Approved for public release; further dissemination unlimited. 

![](images/tmpfjnpspht.pdf-0001-06.png)

Issued by Sandia National Laboratories, operated for the United States Department of Energy by Sandia Corporation. 

**NOTICE:** This report was prepared as an account of work sponsored by an agency of the United States Government.  Neither the United States Government, nor any agency thereof, nor any of their employees, nor any of their contractors, subcontractors, or their employees, make any warranty, express or implied, or assume any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represent that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise, does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government, any agency thereof, or any of their contractors or subcontractors.  The views and opinions expressed herein do not necessarily state or reflect those of the United States Government, any agency thereof, or any of their contractors. 

Printed in the United States of America. This report has been reproduced directly from the best available copy. 

Available to DOE and DOE contractors from 

U.S. Department of Energy Office of Scientific and Technical Information P.O. Box 62 Oak Ridge, TN  37831 

Telephone: (865) 576-8401 Facsimile: (865) 576-5728 E-Mail: reports@adonis.osti.gov Online ordering: http://www.osti.gov/bridge 

Available to the public from U.S. Department of Commerce National Technical Information Service 5285 Port Royal Rd. Springfield, VA  22161 

Telephone: (800) 553-6847 Facsimile: (703) 605-6900 E-Mail: orders@ntis.fedworld.gov Online order: http://www.ntis.gov/help/ordermethods.asp?loc=7-4-0#online 

![](images/tmpfjnpspht.pdf-0002-08.png)

## Table of Contents 

|Table of Contents|Table of Contents|Table of Contents|
|---|---|---|
|**TABLE OF CONTENTS ........................................................................................................................................ 3**|||
|**LIST OF FIGURES ................................................................................................................................................. 5**|||
|**LIST OF TABLES ................................................................................................................................................... 7**|||
|**CONCEPT DESIGN FOR A HIGH TEMPERATURE HELIUM BRAYTON CYCLE WITH**|||
|**INTERSTAGE HEATING AND COOLING ........................................................................................................ 9**|||
|**_EXECUTIVE SUMMARY_ ........................................................................................................................................ 9**|||
|**CONCEPT DESIGN FOR A HIGH TEMPERATURE HELIUM BRAYTON CYCLE WITH**|||
|**INTERSTAGE HEATING AND COOLING ...................................................................................................... 14**|||
|**1**|**INTRODUCTION ........................................................................................................................................ 14**||
|**2**|**SUMMARY RESULTS FROM PREVIOUS STUDIES OF INTERSTAGE HEATED AND COOLED**||
|**BRAYTON CYCLES ............................................................................................................................................ 15**|||
||2.1|INITIALSTUDYOBJECTIVES.................................................................................................................. 15|
||2.2|CURRENTSTUDYOBJECTIVES............................................................................................................... 15|
||2.3|BASICIH&C CONCEPT.......................................................................................................................... 16|
||_2.3.1_|_Cycle Efficiency as a Function of Source Temperature ................................................................... 18_|
||_2.3.2_|_Cycle Efficiency as a Function of Number of Compressors and Turbines ....................................... 19_|
||2.4|POWERCONVERSIONUNITDESIGNCONSIDERATIONS.......................................................................... 20|
||_2.4.1_|_Single Shaft versus Multiple Shafts .................................................................................................. 20_|
||_2.4.2_|_Integrated System versus Distributed System ................................................................................... 20_|
||_2.4.3_|_High Temperature Heat Exchangers ................................................................................................ 21_|
||_2.4.4_|_Pressure Boundary Design Issues .................................................................................................... 21_|
||_2.4.5_|_Horizontal Shaft Designs ................................................................................................................. 22_|
|**3**|**IHC**|**BRAYTON CYCLE LOOPS .............................................................................................................. 25**|
||3.1|PRACTICALLIMITATIONS FOR THE THREEBASELINECBC CONFIGURATIONS....................................... 25|
||_3.1.1_|_Pressure Ratio and Reactor Inlet temperature ................................................................................. 26_|
||_3.1.2_|_Results of “Ideal” Cycle analysis for the Three IHC CBC Brayton Loops ...................................... 29_|
||_3.1.3_|_Example Design for a Mulit-Stage IHC Helium Cooled Brayton Cycle (6c/3t) ............................... 32_|
|**4**|**IMPACT OF TURBOMACHINERY ON THE DESIGN ON THE IHC BRAYTON CYCLE ............ 34**||
||4.1|SIMILARITYCONCEPT FORTURBOMACHINERYDESIGN........................................................................ 34|
||4.2|EFFECT OFSYSTEMCONSTRAINTS ON THETURBOMACHINERYDESIGN................................................ 40|
||_4.2.1_|_Primary Circuit Temperature Constraints ....................................................................................... 40_|
||_4.2.2_|_Grid Connection Constraints ........................................................................................................... 41_|
||_4.2.3_|_Pressure Ratio Constraints .............................................................................................................. 41_|
||_4.2.4_|_Analysis Method used to Determine IHC Brayton cycle Behavior and Turbomachinery predict_|
||_Constraints ..................................................................................................................................................... 41_||
||_4.2.5_|_Mass Flow Rate in the Brayton Cycles ............................................................................................ 42_|
||4.3|ESTIMATE OF THESPECIFICSPEED ANDEFFICIENCY OFTURBOMACHINERY FOR THETHREEIHC CBC|
||SYSTEMS.............................................................................................................................................................. 43||
||4.4|SUMMARYRESULTS FROMSIMILARITYANALYSISAPPLIED TO THETHREEICH BRAYTONCYCLES.... 44|
||_4.4.1_|_High Speed Turbomachinery and Frequency Conversion ............................................................... 45_|
||4.5|HEATEXCHANGEREFFECTS ONDESIGN............................................................................................... 46|
||_4.5.1_|_Heat Exchanger Model Description ................................................................................................. 46_|
||_4.5.2_|_Example Results for the Heat Exchangers ....................................................................................... 47_|
||_4.5.3_|_Heat Transfer in Mixed He/Ar gas Coolants .................................................................................... 52_|
||_4.5.4_|_Impact of Pressure on the Mass of the Heat Exchangers ................................................................. 53_|
||_4.5.5_|_Primary Loop and Circulator Efficiency.......................................................................................... 53_|
|**5**|**CHAPMAN ENSKOG THEORY FOR PROPERTIES OF MIXED GASES ........................................ 54**||

||5.1|GASMATERIALPROPERTIES FORIDEAL ANDMONATOMICGASES....................................................... 55|
|---|---|---|
||5.2|CHAPMANEQUATION FORCP,K,ANDVISCOSITY FORGASES............................................................... 56|
||5.3|MIXTURERULES FOR THEHE/AR GAS MIXTURE.................................................................................... 57|
|**6**|**PERFORMANCE AND SIZING ESTIMATES FOR THREE IHC BRAYTON CYCLES ................. 60**||
||6.1|TABLES OFHEATEXCHANGERMASSCOMPARISONS SHOWING THESTRONGPRESSURESENSITIVITY.. 63|
||6.2|PERFORMANCE FOR THE1C/1TSIMPLERECUPERATEDBRAYTONCYCLE............................................. 67|
||_6.2.1_|_Helium Argon Gas Mixture Configuration ...................................................................................... 68_|
||6.3|PERFORMANCE FOR THE2C/1TSINGLEINTERCOOLERGASBRAYTONCYCLE....................................... 70|
||_6.3.1_|_Helium Argon Gas Mixture Configuration ...................................................................................... 71_|
||6.4|PERFORMANCE FOR THE6C/3TIHC BRAYTONCYCLE.......................................................................... 73|
||_6.4.1_|_Helium Argon Gas Mixture Configuration for the 6c/3t IHC Loop ................................................. 74_|
|**7**|**COST PERFORMANCE AND TRADES .................................................................................................. 77**||
||7.1|RELATIVE COSTAPPROACH................................................................................................................... 78|
||7.2|ANALYSISSEQUENCE............................................................................................................................ 79|
||7.3|COMPONENTCOSTRELATIONSHIPS....................................................................................................... 80|
||_7.3.1_|_Heat Exchanger Costs ...................................................................................................................... 80_|
||_7.3.2_|_Turbines/Compressor Costs ............................................................................................................. 84_|
||_7.3.3_|_Generator Costs ............................................................................................................................... 85_|
||_7.3.4_|_Heat Rejection Heat Exchangers ..................................................................................................... 86_|
||7.4|DESCRIPTION OFCYCLECONFIGURATION............................................................................................. 87|
||7.5|PRELIMINARYCOSTCOMPARISONS....................................................................................................... 87|
||7.6|CYCLEOPTIMIZATIONCONSIDERATIONS.............................................................................................. 88|
||7.7|FIGURE OFMERITSUMMARY ANDOBSERVATIONS............................................................................... 90|
|**8**|**SUMMARY AND CONCLUSIONS ........................................................................................................... 91**||

## List of Figures 

FIGURE 2.1 SCHEMATIC AND T-S DIAGRAM FOR A TYPICAL RECUPERATED BRAYTON CYCLE OPERATING BETWEEN 5 AND 10 MPA WITH SOURCE TEMPERATURE OF 1000K AND SINK TEMPERATURE OF 300K .............................. 17 FIGURE 2.2 SCHEMATIC AND T-S DIAGRAM FOR A 4C/3T IH&C BRAYTON CYCLE OPERATING BETWEEN 2 AND 10 MPA WITH SOURCE TEMPERATURE OF 1000K AND SINK TEMPERATURE OF 300K ........................................... 17 FIGURE 2.3 CYCLE EFFICIENCY AS A FUNCTION OF SOURCE TEMPERATURE FOR THREE PROMISING BRAYTON CYCLES ........................................................................................................................................................................ 18 FIGURE 2.4: THERMAL EFFICIENCY VARIATION WITH THE NUMBERS OF EXPANSION STAGES AND COMPRESSION STAGES FOR A VHTR WITH  (TIT=1025 C). IHC COOLING OPTIONS WITH 1T/1C, 1T/2C, AND 3T/6C APPEAR TO BE THE SYSTEMS THAT NEED FURTHER EVALUATION. ..................................................................................... 19 FIGURE 2.5 PRINTED CIRCUIT (HEATRIC) HEAT EXCHANGER CROSS SECTION AND LAYOUT. (HEATRIC, 2006) ........ 21 FIGURE 2.6: SCHEMATIC FLOW DIAGRAM FOR THE DISTRIBUTED THREE HORIZONTAL-SHAFT MULTIPLE-REHEAT CYCLE, USING THREE PCU MODULES (HP, MP, AND LP) EACH CONTAINING A GENERATOR (G), TURBINE (T), COMPRESSOR (C), AND HEATER AND COOLER HEAT EXCHANGERS, WITH A RECUPERATOR (R) LOCATED IN A FOURTH VESSEL. .............................................................................................................................................. 22 FIGURE 2.7: SCHEMATIC FLOW DIAGRAM FOR THE DISTRIBUTED SINGLE HORIZONTAL-SHAFT MULTIPLE-REHEAT CYCLE WITH ONE TURBINE VESSEL, PRESSURE DECREASES FROM 1 TO 6. ........................................................ 23 FIGURE 2.8 SCHEMATIC FLOW DIAGRAM FOR THE DISTRIBUTED SINGLE HORIZONTAL-SHAFT MULTIPLE-REHEAT CYCLE WITH THREE CASING TURBINE VESSELS, PRESSURE DECREASES FROM 1 TO 6. ...................................... 24 FIGURE 2.9 TURBO-GENERATOR SET FOR THE FIN 5 (EPR) - 1600 MW(E), WITH ONE HP TURBINE AND THREE LP TURBINES. ....................................................................................................................................................... 24 FIGURE 3.1: SIMPLE RECUPERATOR CLOSED BRAYTON CYCLE (CBC) HAVING ONE TURBINE AND ONE COMPRESSOR. (1C/1T CBC CONFIGURATION). ....................................................................................................................... 27 FIGURE 3.2: SINGLE INTERCOOLER CLOSED BRAYTON CYCLE (CBC) HAVING ONE TURBINE AND TWO COMPRESSORS. (2C/1T CBC CONFIGURATION OR  ONE STAGE OF INTERCOOLING, EVEN THOUGH TWO COOLERS ARE USED). ...................................................................................................................................................... 27 FIGURE 3.3: MULTIPLE IHC CLOSED BRAYTON CYCLE (CBC) HAVING THREE TURBINE SETS AND SIX COMPRESSOR SETS. (6C/3T CBC CONFIGURATION). ............................................................................................................. 28 FIGURE 3.4: CYCLE EFFICIENCY AS A FUNCTION OF SYSTEM PRESSURE RATIO FOR VARIOUS BRAYTON CYCLES ..... 31 FIGURE 3.5: GENERAL LAYOUT OF THE 6C/3T IHC GAS BRAYTON LOOP. THE FIGURE IDENTIFIES THE TURBINES AND COMPRESSORS. ................................................................................................................................................ 32 FIGURE 3.6: TYPICAL TEMPERATURES AND GAS FLOW RATES FOR A HELIUM COOLED 6C/3T GAS BRAYTON CYCLE.33 FIGURE 4.1 SPECIFIC SPEED & DIAMETER (NS DS ) DIAGRAM FOR SINGLE STAGE TURBINES AND EXPANDERS OPERATING WITH COMPRESSIBLE FLUIDS. ....................................................................................................... 37 FIGURE 4.2: SPECIFIC SPEED & DIAMETER (NS DS ) DIAGRAM FOR SINGLE STAGE COMPRESSORS (BALJE, 1981). .... 38 FIGURE 4.3: COMPRESSOR TOTAL-TO-STATIC EFFICIENCY SHOWN AS A FUNCTION OF SPECIFIC SPEED ASSUMING THAT THE IDEAL SPECIFIC DIAMETER IS ALSO SELECTED. THE TERM FEFFTM=1.02 IS USED TO INCREASE THE EFFICIENCY BY 2% ASSUMING THAT ADVANCED TURBOMACHINERY DESIGN METHODS ARE USED TO DEVELOP THE COMPRESSOR. ........................................................................................................................................... 39 FIGURE 4.4: TURBINE TOTAL-TO-STATIC EFFICIENCY SHOWN AS A FUNCTION OF SPECIFIC SPEED ASSUMING THAT THE IDEAL SPECIFIC DIAMETER IS ALSO SELECTED. THE TERM FEFFTM=1.02 IS USED TO INCREASE THE EFFICIENCY BY 2% ASSUMING THAT ADVANCED TURBOMACHINERY DESIGN METHODS ARE USED TO DEVELOP THE TURBINE. .................................................................................................................................................. 40 FIGURE 4.5: FRACTIONAL POWER LOST TO CIRCULATOR INEFFICIENCY AS A FUNCTION OF PRESSURE DROP IN THE CORE AND PRIMARY HEAT EXCHANGER. .......................................................................................................... 54 FIGURE 5.1: MIXED GAS THERMAL CONDUCTIVITY, VISCOSITY, AND PRANDTL NUMBER VERSUS TEMPERATURE OR AS A FUNCTION OF HELIUM MOLE FRACTION IN A HELIUM ARGON GAS MIXTURE. .......................................... 59 FIGURE 6.1: CONCEPTUAL LAYOUT OF 6C/3T INTERSTAGE HEATING AND COOLING BRAYTON CYCLE. THE DIMENSIONS ARE APPROXIMATELY 48 M X 44 M .............................................................................................. 63 FIGURE 6.2: SIMPLE RECUPERATOR CLOSED BRAYTON CYCLE (CBC) HAVING ONE TURBINE AND ONE COMPRESSOR. (1C/1T CBC CONFIGURATION). ....................................................................................................................... 67 FIGURE 6.3: SINGLE INTERCOOLER CLOSED BRAYTON CYCLE (CBC) HAVING ONE TURBINE AND TWO COMPRESSORS. IN THIS REPORT IT IS IDENTIFIED AS THE 2C/1T CBC CONFIGURATION OR SOMETIME AS THE SYSTEM HAVING ONE STAGE OF INTERCOOLING, EVEN THOUGH TWO COOLERS ARE USED. ............................. 71 

FIGURE 6.4: MULTIPLE IHC CLOSED BRAYTON CYCLE (CBC) HAVING THREE TURBINE SETS AND SIX COMPRESSOR SETS. (6C/3T CBC CONFIGURATION). ............................................................................................................. 74 FIGURE 7.1: PER UNIT COST OF SMALL SCALE (<1MW) COMMERCIAL GENERATORS AS A FUNCTION OF POWER OUTPUT ........................................................................................................................................................... 86 FIGURE 7.2: PER UNIT COST OF COMMERCIAL COOLING TOWERS AS A FUNCTION OF SIZE. ....................................... 87 FIGURE 7.3: FOM FOR DIRECT CYCLE HELIUM RECUPERATED BRAYTON AS A FUNCTION OF THE RECUPERATOR EFFECTIVENESS. .............................................................................................................................................. 89 FIGURE 7.4: FOM FOR 3T/6C HE/AR BRAYTON AS A FUNCTION OF INPUT HX EFFECTIVENESS WITH HX FLOW PATH HYDRAULIC DIAMETER HELD CONSTANT. ........................................................................................................ 90 

## List of Tables 

TABLE 3-1: TYPICAL CYCLE ANALYSIS SHOWING GAS TEMPERATURES, EFFICIENCIES, AND POWER GENERATION FOR THREE “IDEAL” CBC IHC SYSTEMS. PRESSURE RATIOS ARE ADJUSTED TO ABOUT 3.4-3.5 TO LIMIT THE REACTOR INLET TEMPERATURE TO ABOUT 500 C = 773K. .............................................................................. 30 TABLE 4-1: IHC GAS BRAYTON CYCLE MASS FLOW RATES FOR THE THREE BRAYTON LOOPS, AND FOR PURE HELIUM AND FOR A 70/30 HE/AR GAS MIXTURE. .......................................................................................................... 42 TABLE 4-2: COMPARISON OF AVERAGE COMPRESSOR EFFICIENCIES IN THREE GAS BRAYTON LOOPS (6C/3T, 2C/1T, 1C/1T) FOR 100% HE AND A GAS MIXTURE OF 70% HE 30% AR. .................................................................... 43 TABLE 4-3: COMPARISON OF AVERAGE TURBINE EFFICIENCIES IN THREE GAS BRAYTON LOOPS (6C/3T, 2C/1T, 1C/1T) FOR 100% HE AND A GAS MIXTURE OF 70% HE 30% AR. .................................................................... 43 TABLE 4-4: NOMENCLATURE USED FOR THE DESIGN OF THE HEAT EXCHANGERS. ................................................... 47 TABLE 4-5: GAS COOLER/CHILLER HEAT EXCHANGER RESULTS FOR A 70/30 HE/AR GAS MIXTURE FOR A FRACTIONAL DP OF 1.5% WITH  A 95% EFFECTIVE HEAT EXCHANGERS AND A 90 % EFFECTIVE RECUPERATOR. ........................................................................................................................................................................ 48 TABLE 4-6: GAS HEATER/RE-HEATER AND RECUPERATOR HEAT EXCHANGER RESULTS FOR A 70/30 HE/AR GAS MIXTURE FOR A 1.5% FRACTIONAL DP WITH  A 95% EFFECTIVE HEAT EXCHANGERS AND A 90 % EFFECTIVE RECUPERATOR.. ............................................................................................................................................... 49 TABLE 4-7: GAS COOLER/CHILLER INTERCOOLER HEAT EXCHANGER RESULTS FOR A PURE HELIUM COOLANT. ...... 50 TABLE 4-8: : GAS HEATER/RE-HEATER AND RECUPERATOR HEAT EXCHANGER RESULTS WITH PURE HELIUM AND FOR A 0.5% FRACTIONAL DP. .......................................................................................................................... 51 TABLE 4-9: COMPARISON OF THERMAL CONDUCTIVITY, REYNOLDS NUMBER, AND HEAT TRANSFER COEFFICIENT IN THE PRIMARY CIRCUIT HEAT EXCHANGER FOR THE IHC 6C/3T LOOP WITH HELIUM AND HE/AR 70/30 GAS MIXTURE. ........................................................................................................................................................ 52 TABLE 4-10: COMPARISON OF THERMAL CONDUCTIVITY, REYNOLDS NUMBER, AND HEAT TRANSFER COEFFICIENT IN THE GAS LEG OF THE GAS PRECOOLER AND INTERCOOLERS FOR THE IHC 6C/3T LOOP WITH HELIUM AND HE/AR 70/30 GAS MIXTURE. ............................................................................................................................ 52 TABLE 4-11: PERFORMANCE CHARACTERISTICS OF THE PRIMARY HELIUM GAS LOOP. ............................................. 54 TABLE 5-1: IDEAL GAS PROPERTIES FOR HELIUM AND ARGON AND THEIR MIXTURE AT 70.0 A% HELIUM. ............... 55 TABLE 5-2: DENSITY, SPEED OF SOUND, AND HEAT CAPACITY EQUATIONS FOR IDEAL GASES WITH THE HEAT CAPACITY OF  HE/AR AT 70.0 A% LISTED. ....................................................................................................... 56 TABLE 6-1: SUMMARY PERFORMANCE ESTIMATES GIVING THE ELECTRICAL EFFICIENCY AND THE TOTAL HEAT EXCHANGER MASS USED IN HE/AR GAS MIXTURE AND PURE HELIUM BRAYTON CYCLES FOR THE THREE CONCEPTS. ...................................................................................................................................................... 61 TABLE 6-2: NUMBER OF COMPRESSOR AND TURBINE STAGES FOR THE THREE CONCEPTS. COST ESTIMATES WILL BE PROPORTIONAL TO THE NUMBER OF STAGES FOR EACH CONCEPT. THE SAME NUMBER OF BLADE ROW SET (STATOR + ROTOR) IS USED FOR THE HE/AR AND THE PURE HELIUM GAS TYPE. .............................................. 61 TABLE 6-3: DIAMETER OF COMPRESSOR AND TURBINE WHEELS. ESTIMATES WERE MADE FOR THE FIRST WHEEL PAIR (ROTOR/STATOR) FOR THE COMPRESSOR AND THE LAST WHEEL PAIR (STATOR/ROTOR) FOR THE TURBINES. ....................................................................................................................................................... 62 TABLE 6-4: INLET AND OUTLET PRESSURES FOR THE COMPRESSORS AND TURBINES. SAME VALUES ARE USED FOR HE/AR COOLANT AND THE HELIUM COOLANT. PRESSURES ARE IN KPA. ........................................................ 62 TABLE 6-5: COMPARISON OF THE HEATER AND COOLER HEAT EXCHANGER MASS IN THE 6C/3T IHC BRAYTON CYCLE FOR A HE/AR GAS MIXTURE OF 70/30 MOLE PERCENT (TOP IMAGE) AND FOR PURE HELIUM (BOTTOM IMAGE). ........................................................................................................................................................... 64 TABLE 6-6: COMPARISON OF THE HEATER AND COOLER HEAT EXCHANGER MASS IN THE 2C/1T  BRAYTON CYCLE FOR A HE/AR GAS MIXTURE OF 70/30 MOLE PERCENT (TOP IMAGE) AND FOR PURE HELIUM (BOTTOM IMAGE). THE LOWER PRESSURE LEGS HAVE HIGHER HEAT EXCHANGER MASS. ............................................................. 65 TABLE 6-7: COMPARISON OF THE HEATER AND COOLER HEAT EXCHANGER MASS IN THE 1C/1T (SIMPLE RECUPERATED) BRAYTON CYCLE FOR A HE/AR GAS MIXTURE OF 70/30 MOLE PERCENT (TOP IMAGE) AND FOR PURE HELIUM (BOTTOM IMAGE). NOTE THAT THE LOWER PRESSURE LEGS OF THE LOOP HAVE HIGHER HEAT EXCHANGER MASS. .......................................................................................................................................... 66 TABLE 6-8: DEFINITION OF THE TURBOMACHINERY VARIABLES. SAME NOMENCLATURE IS USED FOR THE OTHER CBC SYSTEMS, BUT SUBSCRIPTS ARE USED TO IDENTIFY THE SPECIFIC COMPRESSOR OR TURBINE. ................ 68 TABLE 6-9: RESULTS OF CYCLE AND TURBOMACHINERY ANALYSIS FOR THE HE/AR SIMPLE RECUPERATED. CYCLE EFFICIENCY AND GAS TEMPERATURES ARE PROVIDED IN THE CYCLE ANALSYS RESULTS. THE TURBINE AND 

COMPRESSOR EFFICIENCIES AND SIZE ESTIMATES ARE GIVEN FOR THE TURBOMACHINERY DESIGN ESTIMATES. CYCLE EFFICIENCY IS 42.8%, COMPRESSOR EFFICIENCY WAS ESTIMATED TO BE 90% AND THE TURBINE EFFICIENCY FOR 10 STAGES WAS ESTIMATED TO BE 86%, HOWEVER BY REDUCING THE NUMBER OF STAGES THE TURBINE EFFICIENCY CAN BE INCREASED TO THE 91% VALUE USED IN THE CYCLE ANALYSIS. ................ 69 TABLE 6-10: THERMAL HYDRAULIC PERFORMANCE DETAILS FOR THE SIMPLE RECUPERATED GAS COOLER, RECUPERATOR AND HEATER WITH A 70/30 HE/ARGON GAS MIXTURE. ............................................................ 70 TABLE 6-11: : RESULTS OF CYCLE AND TURBOMACHINERY ANALYSIS FOR THE HE/AR IHC 2C/1T SYSTEM WITH ONE INTERCOOLER. CYCLE EFFICIENCY IS 45.8%, COMPRESSOR EFFICIENCY WAS ESTIMATED TO BE 89.7% AND THE TURBINE EFFICIENCY WAS ESTIMATED TO BE 92.9%. ........................................................................ 72 TABLE 6-12: THERMAL HYDRAULIC PERFORMANCE DETAILS FOR THE IHC BRAYTON CYCLE WITH A SINGLE INTERCOOLER (2C/1T). THE COOLER DATA IS FOR THE TWO COOLERS AND THE HEATER DATA IS FOR THE HEATER AND THE RECUPERATOR. .................................................................................................................... 73 TABLE 6-13: RESULTS OF CYCLE AND TURBOMACHINERY ANALYSIS FOR THE HE/AR IHC 2C/1T SYSTEM WITH ONE INTERCOOLER. CYCLE EFFICIENCY IS 45.8%, COMPRESSOR EFFICIENCY WAS ESTIMATED TO BE 89.7% AND THE TURBINE EFFICIENCY WAS ESTIMATED TO BE 92.9%. ............................................................................... 75 TABLE 6-14: TURBOMACHINERY EFFICIENCY FOR THE 6C/3T IHC HE/AR BRAYTON CYCLE BASED ON THE SIMILARITY ANALYSIS. ................................................................................................................................... 76 TABLE 6-15; THERMAL HYDRAULIC PERFORMANCE OF THE GAS COOLERS IN THE 6C/3T IHC HE/AR GAS BRAYTON CYCLE ............................................................................................................................................................. 76 TABLE 6-16: THEMAL HYDRAULIC PERFORMANCE OF THE GAS HEATERS AND RE-HEATERS IN THE 6C/3T IHC HE/AR (70/30) GAS BRAYTON CYCLE. ........................................................................................................................ 77 TABLE 7-1: HEAT EXCHANGER CHARACTERISTICS AND RELATIVE COSTS BASED UPON FIXED FLOW LENGTHS. ..... 82 TABLE 7-2: HEAT EXCHANGER CHARACTERISTICS AND RELATIVE COSTS BASED UPON FIXED HYDRAULIC DIAMETER. ...................................................................................................................................................... 83 TABLE 7-3: TURBINE AND COMPRESSOR SIZE DATA FOR THE THREE CYCLES CONSIDERED. ..................................... 85 TABLE 7-4: RELATIVE COMPONENT COST AND FOM FOR HX WITH FIXED FLOW LENGTH. ...................................... 88 TABLE 7-5: RELATIVE COMPONENT COST AND FOM FOR HX WITH FIXED HYDRAULIC DIAMETER. ......................... 88 

## _**Executive Summary**_ 

The primary metric for the viability of these next generation nuclear power plants will be the cost of generated electricity.  One important component in achieving these objectives is the development of power conversion technologies that maximize the electrical power output of these advanced reactors for a given thermal power.  More efficient power conversion systems can directly reduce the cost of nuclear generated electricity and therefore advanced power conversion cycle research is an important area of investigation for the Generation IV Program. 

Brayton cycles using inert or other gas working fluids, have the potential to take advantage of the higher outlet temperature range of Generation IV systems and allow substantial increases in nuclear power conversion efficiency, and potentially reductions in power conversion system capital costs compared to the steam Rankine cycle used in current light water reactors.  For the Very High Temperature Reactor (VHTR), Helium Brayton cycles which can operate in the 900 to 950 C range have been the focus of power conversion research.  Previous Generation IV studies examined several options for He Brayton cycles that could increase efficiency with acceptable capital cost implications.  At these high outlet temperatures, Interstage Heating and Cooling (IHC) was shown to provide significant efficiency improvement (a few to 12%) but required increased system complexity and therefore had potential for increased costs.  These scoping studies identified the potential for increased efficiency, but a more detailed analysis of the turbomachinery and heat exchanger sizes and costs was needed to determine whether this approach could be cost effective. 

The purpose of this study is to examine the turbomachinery and heat exchanger implications of interstage heating and cooling configurations.   In general, this analysis illustrates that these engineering considerations introduce new constraints to the design of IHC systems that may require different power conversion configurations to take advantage of the possible efficiency improvement.  Very high efficiency gains can be achieved with the IHC approach, but this can require large low pressure turbomachinery or heat exchanger components, whose cost may mitigate the efficiency gain.  One stage of interstage cooling is almost always cost effective, but careful optimization of system characteristics is needed for more complex configurations. This report summarizes the primary factors that must be considered in evaluating this approach to more efficient cycles, and the results of the engineering analysis performed to explore these options for Generation IV high temperature reactors. 

Earlier studies focused on thermodynamic cycle analysis to determine Brayton cycle performance.  This approach neglects a number of design constraints imposed by the turbomachinery, especially the system pressure.  In a purely simple thermodynamic cycle analysis the system pressure is undefined, thus it can be selected at will.  However when the turbomachinery is considered the system pressure is highly constrained.  In the more complete 

analysis the system pressure depends on the type of turbomachinery and the frequency at which it spins because strict rules governing the magnitude and orientation of the absolute and relative velocity of the inlet/outlet flow vectors and the blade velocity.  These conditions are governed by dimensionless parameters, _specific speed_ and _dimensionless diameter_ .  For maximum-efficiency-turbines and compressors, the specific speed and specific diameter constrain the system power, pressure, shaft speed, shaft diameter and stage pressure ratio (or temperature ratio) to lie within well defined regions of operation.  In effect these constraints restrict both the system pressure and number of stages required by the turbine and compressor. A conventional Brayton cycle configuration uses a single turbine set (single expansion) and a single compressor (single compression set).  In contrast an IHC configuration uses multiple sets of interstage heating and interstage cooling.  The average temperature of the expansion in the turbine is higher due to interstage heating, and the average temperature of rejection is lower due to interstage cooling for the IHC system versus the simple recuperated Brayton system. This results in more Carnot like configuration and consequently in a higher efficiency at the cost of the additional heat exchangers and the associated ducting. 

The main conclusion obtained from this analysis of turbomachinery design constraints in the evaluation of gas Brayton systems is that in general the high efficiencies assumed in the simple thermodynamic cycle analysis can in fact be achieved.   However to achieve these high efficiencies the designer must change the coolant molecular weight for systems that are grid connected and take the heat exchanger mass penalty associated with lower gas thermal conductivity.  The other alternative is to increase the turbomachinery shaft speed and take the penalty associated with frequency conversion.  The first approach improves efficiency but results in a mass increase, the second approach has off setting characteristics with respect to efficiency increases because the higher speed improves the efficiency but this “advantage” may be reduced by the need to provide frequency conversion and the efficiency penalty associated with this.  In addition higher frequency turbomachinery will be smaller is size, thus will have lower costs, but again this is offset by the need to purchase frequency conversion hardware. 

There are a number of benefits in changing the molecular weight in the fashion just mentioned for grid connected systems.  These include: 

- The total cycle efficiency is greatly improved because the ideal specific speed can be obtained and high efficiency turbines and compressors can be developed. 

- The gas molecular weight can be made closer to the molecular weight of air or steam than when pure helium was used.  In fact if desired the molecular weight can be adjusted to match the molecular weight of air or steam exactly while still keeping the specific speed at its optimum value.  It may be desirable to match the molecular weight of air or steam because the industry base and design tools have been optimized for these molecular weights. 

- In addition increasing the molecular weight also provides more flexibility in the design as the number of stages used in each turbine or compressor set can be reduced.  In effect the higher volumetric flow rate term in the numerator of the specific speed equation permits a larger pressure ratio (and thus the temperature rise) per individual stage within each compressor set.   Typically the stage pressure ratio in an axial machine varies for 1.05 to 1.2, and the total number of stages is limited to around 20 or 30 at most.  (In the analysis reported here the maximum number of stages allowed is 30.) 

- The gas thermal conductivity is kept high because for the same molecular weight the He/Ar gas mixture will have a higher conductivity than a pure gas at the same molecular weight.  The high density of the fluid and high velocity increases the density and thus the Reynolds number thus even though the thermal conductivity of the gas mixture is lower than for helium.  Its impact on the heat exchangers is more complex however as a 70/30 He/Ar gas mixtures has a greater heat transfer coefficient in the intercoolers but a smaller heat transfer coefficient in the gas heaters. 

- Lastly, the gas mixture molecular weight can be easily changed to “dial” in the optimum efficiency. 

For the IH&C Brayton cycle the major components driving the PCS costs are turbines, compressors, generators, recuperation heat exchanger, rejection heat exchangers, input heat exchangers, cooling towers, electrical generator.  Relative estimates of these cost drivers were used to compare a standard recuperated Brayton cycle to the IHC Brayton cycle.  Absolute cost estimates for the major components of a high temperature Brayton cycle at this stage of development are clearly uncertain, but the relative cost comparison of similar cycles (standard recuperated versus IHC) should provide a basis for evaluating the merit of these advanced cycles for next generation reactors. 

Since the goal was to provide a cost relevant figure of merit that can be used to identify the more promising research paths for Generation IV, an incremental cost benefit approach was developed based on changes from a reference recuperated helium Brayton cycle.  Costs for a similar system were developed in the GCRA study which provided a reasonable baseline for modified cycle cost comparisons.  Although any such approach will involve degrees of approximation, the approach of using incremental costs compared to a better defined baseline should be applicable for a reasonable range of assumptions. 

For this initial analysis, a Figure of Merit (FOM) will be defined as the relative cost of electricity from the IH&C cycle as compared to the reference (baseline) recuperated Brayton cycle under the same conditions to pay off the capital investment. 

- FOM = ($/kWhr IH&C/ $/kWhr reference) 

The FOM directly relates to a reduced or increased cost of generated electricity.  (FOM of less than 1 = reduced generation costs). To relate this FOM to cycle efficiency and the PCS costs, the following simplified definitions will be used: 

- ($/kWhr = (RX + PCS) / (Pth*eff*D) 

The FOM obtained for the IHC configurations used as a baseline were near unity – the benefit of increased efficiency was offset by the estimated costs of the larger turbomachinery and heat exchangers.  A key conclusion of this study is that the higher efficiencies can be achieved, but it will require different Brayton cycle configurations to take advantage of the potential of IHC. Based on the configurations evaluated, the more detailed constraints placed on the cycle analysis by the reactor temperature constraints and the turbomachinery requirements significantly reduce the cost benefit of the IHC approach for the conventional configurations. This preliminary evaluation illustrates the complexity when turbomachinery design 

considerations (pressure drops, tip speeds, number of stages, blade lengths) are explicitly included in the cycle analysis.  Other configurations (less common but still within current capabilities), such as dual shaft arrangements, where the first turbine drives multiple compressors (and perhaps a high frequency generator/motor for control) and the second turbine drives a 60 Hz generator, the IHC modifications would involve less cost penalties and still achieve the higher efficiency.  The next stage of these studies will address these options. 

Some of the key observations and conclusions derived from this study are summarized below: 

- Even when constrained by VHTR inlet and outlet temperatures, plant thermal efficiencies can be improved from the low to mid 40% range to the low 50% range with multiple interstage heating and cooling implementation.  Designs for the IHC configurations can be developed that do indeed achieve the high efficiencies that were reported earlier. 

- Multiple techniques can be used to match the specific speed and specific diameter requirement of the turbo/compressor systems.  Changing the molecular weight is one approach that allows the turbine and compressor to operate at specific speeds that allow highly efficient turbomachinery.  Another approach is to spin the turbomachinery faster, but this entails frequency conversion of some type. 

- Primary coolant recirculators appear to be both technically reasonable and not an undue penalty to the system efficiency.  The inefficiencies of the primary gas circulator increases the enthalpy of the primary loop which allows the power conversion system to extract about 40-50% of this energy out as electrical power.  Effective circulator efficiency appears to be as high as 97% based on our similarity analysis modeling approach. 

- The 3t/6c IH&C Brayton cycle system appears to be no larger than current Rankine cycle systems.  Sizes are similar because they have similar pressure in the low pressures leg of the loop. 

- Significant variations in the Figure of Merit (FOM) can be obtained depending upon the design assumptions for the system heat exchangers (two assumptions were used in this report).  Due to the complexity of the 6c/3t IHC Brayton system a large number of parameters may be varied to optimize for system costs.  The systems evaluated in this report are clearly not optimized, but are intended to represent a reasonable operating configuration. 

- The 3t/6c IHC system as proposed here appears to be a marginal cost benefit. Other configurations are suggested by these analyses may offer better cost benefits. These could include systems with two turbines and four or more compressors.  Alternatively, the system pressure could be increased.  Likewise a power turbine configuration could be applied that allows the electrical power turbine to spin at 3600 rpm while a second shaft and set of turbines spins at much higher frequency to run the main compressor. 

- A major advantage of the 6c/3t IHC system is that it is very insensitive to pressure drop.  It is also insensitive to the effectiveness of the gas heater/re-heater and precooler/intercooler heat exchanger effectiveness. 

- Other constraints may force the use of IHC systems, including (1) controllability of system, (2) excessive pressure drop in system, and (3) insensitivity to component effectiveness. 

Future work to determine cost effective approaches to more efficiency gas Brayton cycles is warranted.  Based on the analysis performed in this study it was shown that the use of a single stage of intercooling almost always was worth pursuing because of the gain in efficiency comes at very little cost in complexity.  However the analysis also showed that substantial efficiency gains could be achieved with more complex Brayton cycle configurations but at added costs.  For the multistage IHC system with six compressors and three turbines it appears that advantages gained are offset by the additional costs, but there are a number of intermediate IHC systems that should be considered.  Two such systems are obvious candidates.  In the first system two stages of intercooling can be used instead of one stage.  The second improvement on the IHC system is to use a system with two turbines and fours levels of intercooling.  The approach or goal here is to find the optimum configuration that balances additional costs with improvement in efficiency. 

Another system that needs further examination is one that uses two shafts and one stage of re-heat.  In this configuration one shaft spins the main turbine and power generator at 3600 rpm.  The gas molecular weight and number of stages can be used to obtain the correct specific speed and high turbine efficiency for this shaft.  The second shaft spins a compressor and a small non-synchronous generator to control the shaft speed.  This shaft spins over a range of speeds that can be used for load following and for control.  Because it spins faster than 3600 rpm it can be made smaller and at reduced costs.  This design introduces a level of flexibility and control not available to the single shaft system. 

Finally, another alternative power conversion configuration uses bottoming cycles.. Designs that use steam as the bottoming cycle are all readying being proposed by the European fast gas reactor concept (Mictchell, 2006).  However, it is warranted to examine supercritical CO2 or other supercritical fluids (generally high molecular weight refrigerants) as the bottoming cycle.  We have only briefly looked at these systems and can see that thermal matching and the magnitude of recuperation are important issues that impact the cycle efficiency for these bottoming cycles. 

## **1 Introduction** 

Next generation nuclear power plants should be cost effective and more efficient, with sustainable, proliferation resistant fuel cycles, and reduced environmental impact.  The primary metric for the viability of these next generation systems will be the cost of generated electricity.  One of the important component in achieving these objectives is the development of power conversion technologies that maximize the electrical power output of these advanced reactors for a given thermal power.  More efficient power conversion systems can directly reduce the cost of nuclear generated electricity and therefore advanced power conversion cycle research is an important area of investigation for the Generation IV Program. 

Brayton cycles using inert or other gas working fluids, have the potential to take advantage of the higher outlet temperature range of Generation IV systems and allow substantial increases in nuclear power conversion efficiency, and potentially reductions in power conversion system capital costs compared to the steam Rankine cycle used in current light water reactors.  For the Very High Temperature Reactor (VHTR), Helium Brayton cycles which can operate in the 900 to 950 C range have been the focus of power conversion research.  Previous Generation IV studies examined several options for He Brayton cycles that could increase efficiency with acceptable capital cost implications.  At these high outlet temperatures, Interstage Heating and Cooling (IHC) was shown to provide significant efficiency improvement (a few to 12%) but required increased system complexity and therefore had potential for increased costs.  These scoping studies identified the potential for increased efficiency, but a more detailed analysis of the turbomachinery and heat exchanger sizes and costs was needed to determine whether this approach could be cost effective. 

The purpose of this study is to examine the turbomachinery and heat exchanger implications of these interstage heating and cooling configurations.   In general, this analysis illustrates that these engineering considerations introduce new constraints to the design of IHC systems that may require different power conversion configurations to take advantage of the possible efficiency improvement.  Very high efficiency gains can be achieved with the IHC approach, but this can require large low pressure turbomachinery or heat exchanger components, whose cost may mitigate the efficiency gain.  One stage of interstage cooling is almost always cost effective, but careful optimization of system characteristics is needed for more complex configurations.   This report summarizes the primary factors that must be considered in evaluating this approach to more efficient cycles, and the results of the engineering analysis performed to explore these options for Generation IV high temperature reactors. 

## **2 Summary Results from Previous Studies of Interstage Heated and Cooled Brayton Cycles** 

## _**2.1 Initial Study Objectives**_ 

A previous study (Peterson, Zhao, Vernon and Pickard, 2005) examined a number of engineering trade-offs for the IHC Brayton cycle for high temperature gas cooled reactors. In this earlier study several engineering configurations were examined using thermo-dynamic cycle analysis to understand how the efficiency was affected by the various trade-offs.   In most cases highly efficient turbo-machinery was assumed as were highly effective recuperators and heat exchangers.  A variety of Brayton cycle configurations were examined including simple recuperated configurations, and interstage heated and interstage cooled systems with various numbers of turbines and inter heaters along with various numbers of compressors and inter-coolers. This earlier study showed that interstage heating and cooling is one approach for an advanced Brayton cycle that can provide significant efficiency improvement but requires additional turbines, compressors, heat exchangers and associated ducting that must be accounted for in the evaluation of cost benefit. 

## _**2.2 Current Study Objectives**_ 

In this study, the focus is on examining the constraints on turbomachinery and the heat exchanger sizes and characteristics required to achieve the high efficiencies that are predicted from the earlier scoping analysis.   Other goals include determining sensitivity to the additional pressure drops caused by the more complex ducting and heat exchangers, and to the bypass flow within the turbines and compressors.  These more complex systems also require additional hardware which has an impact on facility size, and on facility costs. The additional costs for the components and for the facility can then be compared with the additional revenue that results from higher efficiency operation. 

To perform this analysis a more detailed conceptual design must be developed  that includes the size of the turbo-machinery, the number of stages, the pressure of the system, the flow rate through the ducting, the ducting lengths, the shaft speeds, and the gas type.  As a starting point the details of the IHC Brayton configuration were restricted to what was viewed as a conservative design.  An IHC gas Brayton system that uses a distributed vs integrated pressure boundary layout, with a horizontal orientation was selected as a reference.  The reactor power was assumed to be 600 MWth to remain consistent with passive cooling mechanisms during loss of flow or loss of heat sink accidents.  We also require that system operate on a single shaft that rotates at 3600 rpm (60 Hz).   In addition the turbine and compressor pressure ratio were selected so that the reactor inlet temperature was sufficiently cool to use inlet flow to cool the pressure boundary.  This allows the use of advanced surperalloys such as Inconel 617 or alloy 265 can be used for the pressure boundary for the reactor.  In addition we have selected an indirect cycle configuration to enhance maintenance and  to prevent fission products from failed fuel from reaching the power conversion plant.  The cost of this additional machinery and the associated performance penalties must be accounted for in the analysis. The analysis summarized in this report expands the previous study to determine the implications of 

turbomachinery and heat exchanger components on overall system efficiency and the assessment of whether the additional costs for components are warranted by the increase in efficiency. 

Detailed designs for major components were developed to determine the geometries of the components to account for the heat transfer capabilities, pressure drops in the ducting and components, and component sizing based on flow rate and system pressure.  This information was used to determine a proposed detailed system layout from which ducting lengths, masses, and pressure drops could also be determined.   The entire IHC system was then analyzed for efficiency taking into account the more realistic pressure drops, duct sizes and lengths, and pressure drop losses due to piping layout and  area changes. Power losses for the primary system were also considered as were efficiencies of the turbo-machinery. 

One major goal of the current study was to include the first order design constraints imposed by the turbomachinery in the system design.  The earlier study used simple thermodynamic cycle analysis to determine the system configuration and efficiency.  This approach unfortunately neglects a number of design constraints imposed by the turbo-machinery, especially the system pressure.  In a purely simple thermodynamic cycle analysis the system pressure is undefined, thus it can be selected at will.  However when the turbo-machinery is considered the system pressure is highly constrained. 

In the more complete analysis the system pressure depends on the type of turbomachinery and the frequency at which it spins because strict rules governing the magnitude and orientation of the absolute and relative velocity of the inlet/outlet flow vectors and the blade velocity.  These conditions are governed by dimensionless parameters, _specific speed_ and _dimensionless diameter_ .  For maximum-efficiency-turbines and compressors, the specific speed and specific diameter constrain the system power, pressure, shaft speed, shaft diameter and stage pressure ratio (or temperature ratio) to lie within well defined regions of operation.  In effect these constraints restrict both the system pressure and number of stages required by the turbine and compressor. 

## _**2.3 Basic IH&C Concept**_ 

This section of the report provides a brief summary of IHC Brayton loops and also summarizes some of the major conclusions made from the earlier study. Figure 2.1 shows a schematic and T-s  (Temperature / Entropy) diagram for a typical recuperated Brayton cycle which uses a single turbine set (single expansion)  and a single compressor (single compression set).  In contrast Figure 2.2 shows a schematic and T-s diagram for an IHC configuration with 3 sets of interstage heating and 4 sets of interstage cooling.  The average temperature of the expansion in the turbine is higher due to interstage heating, and the average temperature of rejection is lower due to interstage cooling for the IHC system versus the simple recuperated Brayton system. This results in more Carnot like configuration and consequently in a higher efficiency at the cost of the additional heat exchangers and the associated ducting. 

![](images/tmpfjnpspht.pdf-0017-00.png)

**----- Start of picture text -----**<br>
1200<br>Turbine Stages<br>Generator<br>1000<br>Gen IV<br>RX 800<br>Heat Sink<br>600<br>Blower<br>400<br>Motor<br>200<br>Compressor Stages<br>19 20 21 22 23 24 25 26 27 28<br>entropy (j/g*K)<br>Temperature (K)<br>**----- End of picture text -----**<br>

**Figure 2.1 Schematic and T-s diagram for a typical recuperated Brayton cycle operating between 5 and 10 MPa with source temperature of 1000K and sink temperature of 300K** 

![](images/tmpfjnpspht.pdf-0017-02.png)

**----- Start of picture text -----**<br>
1200<br>Interstage Heating<br>1000<br>Generator<br>Turbine Stages<br>Gen IV  800<br>RX<br>Heat Sink 600<br>Blower Compressor 400<br>Stages<br>Mo tor<br>200<br>Interstage Cooling 19 20 21 22 23 24 25 26 27 28<br>entropy (j/g*K)<br>Temperature (K)<br>**----- End of picture text -----**<br>

**Figure 2.2 Schematic and T-s diagram for a 4c/3t IH&C Brayton cycle operating between 2 and 10 MPa with source temperature of 1000K and sink temperature of 300K** 

The higher average temperature of expansion is achieved because the pressure ratio used for each stage of compression or expansion is less than in a simple recuperated system. 

The reader should note that block diagram schematics illustrating the simple recuperated Brayton system in Figure 2.1 and in Figure 2.2 show a motor driving the compressor.  This is certainly one possible approach, but because the power required to drive the motor is high the compressor is often attached directly to the same shaft as the turbine and alternator/generator. In the remainder of this report all configurations assume that the turbine and compressor are attached to the same shaft unless stated otherwise. 

For clarity, the number of turbines or compressors will be referred to as “sets”.  Typically a turbine set or compressor set is designated with the letters A, B , C etc. Thus in Figure 2.2 turbine TA is the first turbine set that the flow reaches.  Turbine TB is the second turbine set along the flow path and TC is the third.  The same nomenclature is used for the compressors. However each turbine may use a number of stages. Each stage for a turbine refers to a row of 

rotating and stationary blades. A single turbine may have several “stages” of rotors and stators. The word interstage heating refers to the heat exchanger that is used to reheat the gas after expansion in a previous expansion or recuperation.  Sometimes in this report we will refer to turbine sets and compressor sets with the understanding that even though there may be many stages of rotors and stators in this single turbine set, it has only one stage of interstage heating. 

## **2.3.1 Cycle Efficiency as a Function of Source Temperature** 

All Brayton cycles show increasing efficiency with higher source temperatures. As a starting point the potential cycle efficiencies for various Brayton cycles were first determined.   Figure 2.3  shows the performance trend for the supercritical CO2 Brayton, the single stage recuperated Helium Brayton, and the three turbine/six compressor (3t/6c) IH&C Helium Brayton, all with the same component efficiencies (  c=85%,  t=93%) and heat exchanger effectiveness (  HX_in=95%,  HX_rec=95%,  HX_rej =95%),with a (  fractional pressure drop, with a sink temperature of 27°C and with all cycles optimized for their respective pressure ratio.  Clearly theses values are idealistic but surve to show the potential benefit of these systems.  As technologies improve, these efficiencies will increase, the cost benefit will still drive the decision to implement these technologies. 

## **Cycle Efficiencies vs Source Temperature for fixed component efficiencies and system effectiveness** 

![](images/tmpfjnpspht.pdf-0018-04.png)

**----- Start of picture text -----**<br>
60%<br>50%<br>40%<br>30%<br>20%<br>1t/1c rec He Brayton<br>10% SCSF CO2 Brayton<br>3t/6c IH&C He Brayton<br>0%<br>200 300 400 500 600 700 800 900 1000<br>Source Temperature (°C)<br>Cycle Efficiency (%)<br>**----- End of picture text -----**<br>

**Figure 2.3 Cycle Efficiency as a function of source temperature for three promising Brayton cycles** 

From Figure 2.3 it can be seen that interstage heated and cooled Helium Brayton cycles offer the potential improvement of 15% improvement in efficiency over a simple recuperated Brayton cycle at 600 C and about 12% potential improvement at 900 C.  Also note that below 

source temperatures of 600 C, the supercritical CO2 systems offer substantial advantages over regular recuperated Brayton cycles. 

## **2.3.2 Cycle Efficiency as a Function of Number of Compressors and Turbines** 

The IHC Helium Brayton cycle potentially offers substantial improvements in efficieny when high reactor outlet temperatures very high effectiveness heat exchangers are used.  However this was for a three turbine/six compressor configuration with a total of three heaters and six gas chillers.  The impact on efficiency based on number of turbines and compressors was also evaluated in the earlier study (Peterson, et. al, 2005).  Figure 2.4 illustrates the predicted results as a function of number of turbines for three options, the first option (crosses) represent a system with two turbines per compressor, while the curves with x’s and circles represent systems with one turbine per compressor and one turbine per two compressors.  Clearly systems with one turbine and two compressors provide higher efficiencies regardless of the number of turbines used.  This means that adding more interstage coolers is generally more beneficial than adding more interstage heaters.  (In general there is more benefit to lowering the heat sink temperature by one degree than by raising the source temperature by one degree.) 

![](images/tmpfjnpspht.pdf-0019-03.png)

**----- Start of picture text -----**<br>
3t/6c<br>1t/2c<br>1t/1c<br>**----- End of picture text -----**<br>

**Figure 2.4:  Thermal efficiency variation with the numbers of expansion stages and compression stages for a VHTR with  (TIT=1025 C). IHC cooling options with 1t/1c, 1t/2c, and 3t/6c appear to be the systems that need further evaluation.** 

Based on Figure 2.4 the previous study concluded that using three turbines and six compressors seemed to offer the potential for high efficiency and with reasonable additions to complexity. Industry proposals (GA, and MHTR) often use power conversion systems with one turbine and two compressors and thus use two gas chillers.  (Typically one is called the pre-cooler and the other is called the interstage cooler) This report attempts to quantify this behavior. 

## _**2.4 Power Conversion Unit Design Considerations**_ 

There are several major design choices to make when considering a multiple-reheat helium Brayton power conversion system [Peterson, et al., 2004]: 

- horizontal shaft versus vertical shaft 

- single shaft versus multiple shafts 

- integrated system versus distributed system 

- high temperature heat exchangers selection 

- active pressure vessel cooling 

Each of these issues is briefly described below. 

## **2.4.1 Single Shaft versus Multiple Shafts** 

In single-shaft systems, compressors, turbine, and generator are integrated to a single shaft, which may also include flexible couplings or reducing gears.  In multiple-shaft systems, the design consists of several independent turbomachinery-generator modules arranged in an efficient cluster. Each power conversion unit (PCU) module typical produces equal electrical power. Flow passes through each module and then through an independent recuperator module. The pressure ratio across each module is same and the pressure ratio across the total system is the product of the module pressure ratios.  Within each module, there is one turbine, one heater, two compressors, two coolers and one generator. The current gas turbine industry doesn’t use gears above several 10’s of MW.  Thus for this study where we wish to study systems with 200 MWe, multiple shafts with gears or gear reduction systems are considered not practical. 

Single-shaft systems are potentially easier to control and might have smaller footprints than horizontal multiple-shaft systems. When the total power is large, the PCU pressure vessel becomes very large. This is difficult to construct, especially for an integral vertical single-shaft system. There exist other challenges for single-shaft configurations such as isolating different pressure zones and long shaft rotor dynamics. For a multiple-reheat system, each stage of expansion and compression operates at a different pressure level.  It is highly desirable to separate these different pressure zones so that the pressure boundary can operate at the local compressor cooler inlet pressure and temperature, and the internal hot-duct and turbine-shroud components can operate with minimal pressure differentials to reduce long-term creep deformation. 

## **2.4.2 Integrated System versus Distributed System** 

PCS components can be located inside a single pressure vessel (e.g. GT-MHR), or can be divided among multiple pressure vessels (e.g., PBMR).  This is a major design choice, with important impacts in several other areas of design and maintain. Previous studies developed point designs to compare distributed and integrated PCS designs, and found that the power density and efficiency of the integral and the distributed designs can be comparable. The 

distributed designs require substantially larger volumes for connecting ducts, which is expected due to the greater distances between components. 

## **2.4.3 High Temperature Heat Exchangers** 

All the high temperature heat exchangers are assumed to use ~~c~~ ompact heat exchangers to increase power density. Heaters are the most difficult components to design and manufacture due to their operation at the highest operating temperature and pressure difference. For heat transfer with liquid coolants like liquid salts, heaters will be immerged in high-pressure helium environment to reduce helium flow misdistribution and improve thermal effectiveness. Coolers and recuperator designs can be essentially identical to those for the GT-MHR PCU. 

Compact plate heat exchangers are already commonly used for heat transfer at lower temperatures. Of great interest for advanced high temperature Brayton cycles is the potential to fabricate compact plate type heat exchangers that would provide very high surface area to volume ratios and very small fluid inventories while operating at high temperatures. 

One of near-term choice for high temperature liquid metal to helium heaters are printed ciruit (PCHE) heat exchangers such as Heatric heat exchangers. PCHE are constructed from a process of chemically etching metal plates and diffusion bonding (heatrics.com) as shown in Figure 35. Heater modules can also be arranged in the annual space in a vertical vessel. Helium flows into the heaters from outside and hot helium is collected in the vessel center. 

![](images/tmpfjnpspht.pdf-0021-05.png)

**----- Start of picture text -----**<br>
Flow channels in a PCHE   Plates are stacked then diffusion bonded<br>**----- End of picture text -----**<br>

**Figure 2.5 Printed circuit (Heatric) heat exchanger cross section and layout.  (Heatric, 2006)** 

## **2.4.4 Pressure Boundary Design Issues** 

A major choice for pressure boundary design is the choice of vessel materials that can operate at high temperatures.  Conventional light water reactor (LWR) vessel materials require active cooling by compressor outlet flow.  In practice, for multiple-reheat closed gas cycles, it is easy to develop configurations where the pressure boundary operates at the compressor outlet or recuperator outlet temperature and all hot components are submerged inside the cold boundary. Such a design requires internal forms of insulation and cooling for the pressure boundary.  The cooling can use the compressor outlet gas temperature or external water cooling.  In fact this approach of using internal insulation and pressure boundary cooling has been common design practice for many gas cooled reactors.   In the current study we assume that canned/clad forms of internal insulation are used with water cooled pressure boundaries so that standard seals, o- rings, and closure methods can be applied. 

## **2.4.5 Horizontal Shaft Designs** 

A variety of horizontal shaft configurations are possible.  This sections describes two designs, one that has multiple shafts and the second that has a single shaft. 

## **2.4.5.1 Multiple Horizontal Shaft Designs** 

Figure 40 shows the schematic flow diagram for the distributed three horizontal-shaft multiplereheat cycle, using three PCU modules (HP, MP, and LP) each containing a generator (G), turbine (T), compressor (C), and heater and cooler heat exchangers, and a recuperator (R) located in a separate vessel. The red arrows in the left part of this diagram form the hot flow loop (not a closed loop, but connected to the cold loop in recuperator), within which high temperature helium flows in hot ducts, turbines, and the recuperator. 

The arrangement pattern shown in the diagram is optimized to minimize the total length of hot ducts, which are much more expensive than cold ducts and generate heat losses. All the hot ducts are concentric ducts and cooled by cold helium which flows in the annulus outside hot inner ducts. The blue arrows form a larger cold loops. 

![](images/tmpfjnpspht.pdf-0022-05.png)

**----- Start of picture text -----**<br>
LP<br>T3 C5 C6 G1<br>H3<br>IC5 IC6<br>MP<br>T2 C3 C4 G2<br>R<br>H2<br>IC3 IC4<br>HP<br>T1 C1 C2 G1<br>H1<br>IC1 IC2<br>**----- End of picture text -----**<br>

![](images/tmpfjnpspht.pdf-0022-06.png)

**----- Start of picture text -----**<br>
T: turbine, C: compressor, R: recuperator,<br>H: heater, IC: intercooler, G: generator<br>1 to 6: from high pressure to low pressure<br>**----- End of picture text -----**<br>

**Figure 2.6:  Schematic flow diagram for the distributed three horizontal-shaft multiplereheat cycle, using three PCU modules (HP, MP, and LP) each containing a generator (G), turbine (T), compressor (C), and heater and cooler heat exchangers, with a recuperator (R) located in a fourth vessel.** 

## **2.4.5.2 Single Shaft Horizontal Systems** 

Figure 2.7 shows the schematic flow diagram for the distributed single horizontal-shaft multiple-reheat cycle with a single pressure vessel. All turbomachinery are on the same shaft 

and within a big turbine vessel. The red arrows in the top part of this diagram form the hot flow loop (not a close loop, but connect to cold loop in recuperator), within which high temperature helium flow in hot ducts, turbines, and recuperator. All the hot ducts are concentric ducts and cooled by cold helium which flows in the annulus outside hot inner ducts. The blue arrows form a larger cold loop. The turbine vessel is cooled by the recuperator low pressure side exit flow or externally by water. So the turbine vessel operates at low temperature. The maximum equipment size in this system is the turbine vessel, which has a diameter of 4.6 m and a length of 43 m. One of potential concerns is that HP and MP turbomachinery and inner ducts are not in pressure balance with the turbine vessel inside pressure (LP). Those hot components have to withstand the inner pressures. Overall, this design has inherent drawbacks which cannot be easily solved. Therefore, this case is presented only to show it is not good idea to arrange all the turbomachinery into a single pressure vessel, and instead it is better to provide separate vessels for the HP, MP and LP turbines and compressors, so the vessels can operate at different pressures. 

![](images/tmpfjnpspht.pdf-0023-01.png)

**----- Start of picture text -----**<br>
R<br>H1<br>H3 H2<br>T3 C5 C6 T2 C3 C4 T1 C1 C2 G<br>IC5 IC3 IC1<br>IC4 IC2<br>IC6<br>**----- End of picture text -----**<br>

- **T: turbine, C: compressor, H: heater, IC: cooler, R: recuperator, G: generator 1 to 6: from high pressure to low pressure** 

## **Figure 2.7:  Schematic flow diagram for the distributed single horizontal-shaft multiplereheat cycle with one turbine vessel, pressure decreases from 1 to 6.** 

Figure 2.8 shows a schematic flow diagram for a distributed single horizontal-shaft multiplereheat cycle with three separate turbine vessels. All turbomachinery are on the same shaft but are located in three separate turbine vessels operating at different pressures. This arrangement solves the pressure mismatch problem shown in Figure 2.7. All the hot components now are cooled by cold flow with pressure close to the hot flow. The maximum equipment in this system is LP turbine vessel, which has a diameter of 4.6 m and a length of 17 m. In this configuration, split-casing vessels like those commonly used for steam turbine systems, like the Siemens turbine shown in Figure 2.8, must be used. Split-casing vessels have very large sealing boundaries so that controlling helium leakage may be a potential problem. 

![](images/tmpfjnpspht.pdf-0024-00.png)

**----- Start of picture text -----**<br>
R<br>H1<br>H3 H2<br>T3 C5 C6 T2 C3 C4 T1 C1 C2 G<br>LP MP HP<br>IC5 IC6 IC3 IC4 IC1 IC2<br>**----- End of picture text -----**<br>

**T: turbine, C: compressor, H: heater, IC: cooler, R: recuperator, G: generator 1 to 6: from high pressure to low pressure** 

**Figure 2.8** Schematic flow diagram for the distributed single horizontal-shaft multiple-reheat cycle with three casing turbine vessels, pressure decreases from 1 to 6. 

![](images/tmpfjnpspht.pdf-0024-03.png)

**Figure 2.9  Turbo-generator set for the Fin 5 (EPR) - 1600 MW(e), with one HP turbine and three LP turbines.** 

## **3 IHC Brayton Cycle Loops** 

To determine if the costs associated with IHC closed Brayton cycles are worth the additional revenue that results from the higher efficiency IHC Brayton Loop, several factors must be considered. It is first necessary to develop the conceptual designs of these various systems to such an extent that the limitations of the turbomachinery are taken into account, the loop is sufficiently well defined that the pressure drops can be reasonably estimated by knowing the lengths of ducting and taking into account form losses as well as frictional losses, and lastly to have reasonable estimates for the size/mass and costs of the additional heat exchangers needed for the various IHC closed Brayton loop configurations. 

To accomplish this task three types of Brayton cycle loops were examined.  The first is a simple recuperated Brayton cycle.  This cycle has one turbine and one compressor and is denoted as 1c/1t in many of the plots and tables that follow.  This cycle is the normal recuperated cycle that is first considered for closed Brayton cycles.  A schematic of this loop is illustrated in Figure 3.1.   In this figure and in the following two figures the gas coolant temperature are indicated at station locations around the loop.  Thus station 1 starts at the compressor inlet, station 2 is the compressor outlet which equals the high pressure recuperator leg inlet temperature. Station 3 is the heat exchanger inlet temperature, 4 is the turbine inlet temperature, 5 is the turbine outlet, and 6 is the low pressure recuperator outlet leg.  Subscripts a-f are used to indicate which intercooler-compressor or re-heater-turbine set is being referenced ~~..~~ 

The second loop examined has one stage of intercooling and is illustrated in Figure 3.2.  In reality two coolers are used, one is the pre-cooler or gas-chiller (or Waste heat exchanger), while the other is frequently referred to as the inter-cooler. This second loop is denoted by 2c/1t in this report as there are two compressors and one turbine.  This configuration is frequently proposed for high temperature gas cooled reactors because the additional stage of inter cooling only adds one additional heat exchanger but substantially increases the efficiency of the cycle (see Figure 2.4). 

The last and third type of loop considered uses 6 compressors and 3 turbines and is denoted as 6c/3t and is illustrated in Figure 3.3.  This last loop has two inter-coolers and one precooler.  In essence every compressor has one cooler though standard nomenclature and discussions of these systems use the phrase inter-cooler which refers to the number of coolers that follow the first compressor.  This loop also has two re-heaters (re-heaters follow the first turbine and reheat the coolant after it is has been expanded and cooled in the turbine), but in total one heater is used for each turbine. This concept was identified as the most promising IHC closed Brayton cycle as it offered very high efficiencies, up to 57% for ideal systems having ideal pressure ratios.  The “idea” cycle generally limits pressure drops to 5%, and uses heat exchangers (intercoolers, re-heaters and recuperators) having effectiveness values of 95%. 

## _**3.1 Practical Limitations for the three Baseline CBC Configurations**_ 

In this report the goal is to remove most of these “ideal” assumptions and examine relatively conservative approaches that are straightforward extensions of current industry practice. Generally CBC systems are considered to have the following attributes: 

1. An indirect coolant circuit.  The primary coolant is through the reactor and uses Helium coolant (generally at 7 MPa).  The secondary circuit may be helium or a gas mixture. Electrical cycle efficiency is reduced as it takes electrical power to run the circulator. 

2. The reactor inlet temperature is restricted to be less than 500 C = 773 K so that the inlet coolant can be used to keep the pressure boundaries cool and so that non-refractory metals can be used for the pressure vessel. 

3. The peak pressure in the secondary coolant loop is 7 MPa. 

4. A single shaft system is considered versus multiple shafts. 

5. The shaft speed is 3600 rpm. 

6. The system uses internal insulation to keep the pressure vessel and ducting wall temperature to below the reactor inlet temperature of ~773 K. 

7. Turbine and compressor efficiencies are based on turbomachinery design principles. 

8. Pressure drops are based on predictive estimates based on the length of the ducting, heat exchangers, and form losses. 

In the body of this report, it will be mentioned when there is an option to deviate beyond these restrictions and a brief description of why and when one may want to deviate from these restrictions. 

## **3.1.1 Pressure Ratio and Reactor Inlet temperature** 

The “ideal” cycles that were summarized in the previous section used a turbine pressure that produced the highest efficiency.  In fact real GCR designs use the inlet reactor coolant to keep the ducting and pressure vessel cool and sufficiently cool that the reactor inlet temperature is generally kept below 500 C = 773 K.  (In HTTR is was limited to about 400 C or less.)   For the “ideal” cycles the highest efficiencies for recuperated cycles are achieved for systems having pressure ratios of 1.6-2.0.  In this report we have used pressure ratios are more realistic. We used pressure ratios of 3.4-2.5 because this restricts the reactor inlet temperature to a values that is less than 500 C. The reactor inlet temperature is not explicitly calculated but it is generally 10-30 K above T.3 or close to T.5. 

For consistency with the earlier reports by Peterson, Vernon and Pickard the heat exchangers effectiveness (for all three CBC IHC configurations) are kept at 0.95 as is the recuperator effectiveness.  The turbine is “assumed” to have an isentropic efficiency of 0.93% and the compressor is assumed to have and isentropic of 0.90 %.  The pressure drop for all three CBC IHC configurations is set to a fractional pressure drop of 5%. 

![](images/tmpfjnpspht.pdf-0027-00.png)

**----- Start of picture text -----**<br>
Reactor<br>Trx_in Tsrc<br>Helium<br>3 HTRA<br>Circulator<br>4 Generator<br>70 % Helium<br>30 % /Argon<br>T A C A<br>1<br>5 2<br>Gas Chiller<br>GCXA HX<br>Water Tsnk<br>3 6<br>Recup<br>**----- End of picture text -----**<br>

**Figure 3.1:  Simple recuperator Closed Brayton Cycle (CBC) having one turbine and one compressor.  (1c/1t CBC configuration).** 

![](images/tmpfjnpspht.pdf-0027-02.png)

**----- Start of picture text -----**<br>
Reactor<br>Trx_in Tsrc<br>Helium<br>HTRA<br>Circulator<br>Synchronous<br>Generator<br>70 % Helium<br>30 % /Argon<br>T A C B C A<br>Gas Chiller<br>GCXB GCXA HX<br>Water Tsnk<br>Recup<br>Helium / Argon<br>**----- End of picture text -----**<br>

**Figure 3.2:  Single intercooler Closed Brayton Cycle (CBC) having one turbine and two compressors. (2c/1t CBC configuration or  one stage of intercooling, even though two coolers are used).** 

![](images/tmpfjnpspht.pdf-0028-00.png)

**----- Start of picture text -----**<br>
Circulator<br>Trx_in Tsrc<br>Reactor<br>3 HTRA HTRB HTRC<br>4a 4b 4c<br>5<br>T A C F C E TB CD CC TC C B CA<br>1f 1e 1d 1c 1b 1a<br>GCXF GCXE GCXD GCXC GCXB GCXA<br>Tsnk<br>6 Water<br>3 5<br>3<br>Recuperator<br>6<br>2<br>**----- End of picture text -----**<br>

**Figure 3.3:  Multiple IHC Closed Brayton Cycle (CBC) having three turbine sets and six compressor sets.  (6c/3t CBC configuration).** 

## **3.1.2 Results of “Ideal” Cycle analysis for the Three IHC CBC Brayton Loops** 

Table 3-1 provides the results of the cycle analysis for the three “ideal” Brayton cycles.  This analysis uses a larger pressure ratio that used before, and it also accounts for inefficienies that result from using an indirect cycle.  The power efficiency of the recirculator is described be low but was predicted to cause a 3% decrement in efficiency.  Likewise the efficiency of the generator was included and it was assumed to be 98%.  The cycle efficiencies for the three systems are   56.3%, 53% and 44% for the three systems starting with the more complex IHC system and moving toward the simplest system.  The cycle efficiency are based on reactor power which was assumed to be 600 MW for all systems, but because the circulator is about 97% efficient, approximately 3% of the thermal power shows up as additional heat in the loop, thus the heat delivered to the primary heat exchangers is about 617-618 MWth.  The electrical efficiencies are lower that the cycle efficiency, and these values are 53%, 50%, and 43%. These values appear reasonable for this stage of analysis.  It is also assumed that about 1% of the electrical power will be required for cooling of other structures, thus the Net electrical efficiency for the three system should be on the order of 52%, 49% and 42%.  Again these values are not far from many published numbers for the pebble bed modular reactor. 

For comparison purposes results of similar cycle calculations for the same input parameters as used by Peterson are provided in Table 3-1.  Note that the results in table 3-1 use a coolant gas mixture of 70% He and 30% (mole fraction) of Argon, while those in table 3-2 are in Helium. The pure cycle analysis doesn’t depend on the gas type except for the ratio of the specific heat at constant pressure to constant volume.  For ideal gases and gas mixtures this is constant at 4/3.  The mass flow rate does depend on the gas type as the heat capacity is a function of molecular weight. 

## **Table 3-1:  Typical cycle analysis showing gas temperatures, efficiencies, and power generation for three “ideal” CBC IHC systems. Pressure ratios are adjusted to about 3.43.5 to limit the reactor inlet temperature to about 500 C = 773K.** 

There are a few important points to note for these systems.  First the 6c/3t IHC loop has a much lower flow rate than the 2c/1t and 1c/1t Brayton loops.  This is because only one heater is used in the two simpler loops while three heaters are used in the 6c/3t IHC loop.  Because three heaters have the same temperature rise across them (to first order) it takes three times less flow than in the simpler systems.  This fact will impact the how efficiency of the turbines and compressors.  Also, the 6c/3t loop has a total pressure ratio of about 3.4[3] =39.3.  This means that even with a peak coolant pressure of 7 MPa, the low pressure leg in the loop is 0.178 MPa. This low pressure which is only 78% above ambient pressure will require large turbomachinery and large heat exchangers when they are used in the low pressure leg of the loop. 

The impact that total pressure ratio has on efficiency is shown in Figure 3.4 (Peterson, 2005). This figure plots the cycle efficiency as a function of total pressure ratio for various IHC systems.  The most relevant curve in this figure is the dark blue line (IHC system with 4c/4t). This curve peaks at a total pressure ratio of about 4, but in the 6c/3t IHC system the total pressure ratio is 39.  Notice that a pressure ratio of 39 (which is not even on the plot) the cycle efficiency is below at or below 50%.  Because the stage pressure ratio is set by the material limits of the primary heat exchanger and the reactor inlet temperature there is no real freedom in the design to lower the total pressure ratio to a value near 4.  Thus, the multi-staged IHC systems will in fact be limited to efficiency near 50%. 

**Brayton Cycle Efficiencies vs Pressure-Ratio for Thermodynamic Cycles Operating between 1173K and 300K** 

![](images/tmpfjnpspht.pdf-0031-03.png)

**----- Start of picture text -----**<br>
80% simple<br>recuperated brayton<br>70%<br>IH&C w 2 st comp & 2 st turbine<br>60% IH&C w 4 st comp & 4 st turbin e<br>50%<br>40%<br>30%<br>20%<br>10%<br>0%<br>0 2 4 6 8 10 12 14 16 18 20<br>pressure-ratio (Phigh/Plow)<br>cycle efficiency<br>**----- End of picture text -----**<br>

**Figure 3.4:  Cycle Efficiency as a function of system pressure ratio for various Brayton cycles** 

## **3.1.3 Example Design for a Mulit-Stage IHC Helium Cooled Brayton Cycle (6c/3t)** 

The general layout of the 6c/3t IHC Brayton loop is provided in Figure 3.5.  This figure is based on Peterson’s configuration (Peterson, 2005) and shows that one turbine is matched to two compressors and all turbo-compressor sets are on  a single shaft.  The high pressure turbomachinery is on the left of the figure and the low pressure (and thus larger) machinery is on the right side of the figure.  This configuration allows for individual pressure containment around each turbo-compressor set. This is important as the pressure ratio is about 39 and leakage from the high leg to the low leg must be minimized.  A similar illustration is provided in Figure 3.6 but the gas temperature state points, mass flow rate and system pressures are shown at the various locations in the loop.  This analysis assumes that helium is the working fluid.  It is seen that because helium has a large heat capacity the mass flow rate around the loop is only 60 kg/s.  In the simpler single turbine gas Brayton systems the mass flow rate is about 3.5 times this value. 

![](images/tmpfjnpspht.pdf-0032-02.png)

**----- Start of picture text -----**<br>
HTRA HTRB HTRC<br>T A C F C E TB CD CC TC C B CA<br>GCXF GCXE GCXD GCXC GCXB GCXA<br>Recuperator<br>**----- End of picture text -----**<br>

**Figure 3.5:  General layout of the 6c/3t IHC Gas Brayton loop. The figure identifies the turbines and compressors.** 

![](images/tmpfjnpspht.pdf-0033-00.png)

**----- Start of picture text -----**<br>
Reactor, 410 MW<br>1190 K 808 K, 3.4 MPa<br>dp/p =.025<br>3.4 MPa 204 kg/s Circulator<br>Pout/Pin=1.04<br>68 kg/s 68 kg/s 68 kg/s<br>795 K 3.4 MPa<br>1190 K 814 K 1190 K 814 K 1190 K<br>HTRA HTRB HTRC<br>1169 K 1169 K 1169 K<br>3.4 MPa 794 K 794 K Generator<br>1.15 MPa 0.38 MPa 200 MWe<br>48.7% eff<br>3.45 MPa 1.99 MPa 1.15 MPa 0.66 MPa 0.38 MPa 0.22 MPa<br>T A C F CE T B C D C C T C C B CA<br>305 K 305 K 305 K<br>0.128 MPa<br>305 K 392 K 392 K 305 K 392 K 392 K 305 K 393 K<br>774 K<br>Gas Chiller<br>3.4 MPa<br>GCXF GCXE GCXD GCXC GCXB GCXA HX<br>300 K<br>68 kg/s<br>Recup 794 K<br>68 kg/s<br>412 K<br>392 K,   3.45 MPa 0.128 MPa<br>**----- End of picture text -----**<br>

**Figure 3.6:  Typical temperatures and gas flow rates for a helium cooled 6c/3t gas Brayton cycle.** 

## **4 Impact of Turbomachinery on the Design on the IHC Brayton Cycle** 

Turbomachinery design has a significant impact on the design of an IHC Brayton cycle. This section addresses the efficiency implications of the turbomachinery design on system efficiency.  In addition the sensitivity of the design to pressure drops caused by additional ducting length or heat exchangers must also be included. Also to the extent possible, the influence of bypass flow within the turbines and compressors must also be accounted for. 

## _**4.1 Similarity Concept for Turbomachinery Design**_ 

Similarity considerations are used to determine the turbomachinery size estimates, the gas pressure levels, the number of stages, and the gas type.  Similarity theory is based on dimensionless analysis called the Buckingham Pi theorem (Buckingham, 1914).  This theory states that machines which are geometrically similar have similar velocity triangles in the flow path.  Thus when they are operated with fluids that have the same/similar thermodynamic fluid properties they will have the same efficiencies (Shepard, 1957).    The word similar here means that both the machine and the properties of the fluid have the same dimensionless parameters. The similarity concept is described in Balje (Balje, 1981). 

Six independent dimensional similarity parameters exist.  They are 1) the efficiency, 2) the machine Reynolds number Re[*] , The Laval number, the ratio of specific heats (  ), the specific speed, and the specific diameter.  The efficiency is just the ratio of actual power produced to the ideal (isentropic) power produced.  The machine Reynolds number is the ratio of the tip speed times the tip diameter divided by the kinetic viscosity.  Typically these values must be > 10[6][for compressible fluids and >10][8][ for incompressible fluids.  The Laval number is the ratio ] of the tip speed to the sound speed at the static gas temperature.  For optimum efficiencies the Laval number must be near 0.6-0.7, which simply means that the tip velocity must be very close to the speed of sound. The specific speed and the specific diameter will be described in more detail in the following paragraphs but they can be used to determine the efficiency of a turbine or compressor because the dimensionless speed and diameter assures that the velocity triangles are similar for machines that have known measured efficiencies for the same dimensionless speed and dimensionless diameter parameter. 

Before describing the dimensionless speed and dimensionless diameter parameters, it is important to introduce a few terms that are frequently used for turbo machinery.  For compressible flow in a compressor or turbine the ratio of the exit temperature (To2 or To5) to the inlet temperature (To5 or T is determined by equations 4-1 and 4-2.   The subscript o refers to the total temperature,  (gamma) is the ratio of the specific heat at constant pressure to constant volume, and  is the efficiency.  When isentropic efficiency values are being referred to we use the subscript s.  The subscript p is used when we are using definitions based on polytropic efficiency.  The subscripts C and T refer to the compressor or the turbine.  These equations are very important because they allow one to relate the temperature ratio, pressure ratio, and the efficiency to any two of these parameters.  Thus if the pressure ratio and the efficiency of a compressor is known, then the temperature ratio can be determined.  Given the temperature ration allows one to calculate the total power given the inlet temperature and mass flow rate by simply calculating mdot*Cp*dT. 

![](images/tmpfjnpspht.pdf-0035-00.png)

For a compressor or turbine the specific speed and the specific diameter are determined by the following two equations. 

![](images/tmpfjnpspht.pdf-0035-02.png)

![](images/tmpfjnpspht.pdf-0035-03.png)

The specific speed relates the shaft speed (Nrev), the volumetric flow rate through the turbomachine, and the adiabatic head (see equation 5-7). It is called specific speed because it proportional to the shaft-speed.  The specific diameter is related to the wheel diameter as well as to the volumetric flow rate and adiabatic head.  It gets its name because it is proportional to the wheel tip diameter.  The volumetric flow rate is defined by equations 5-5 and 5-6, and the adiabatic head is defined in 5-7.  In these equations vdot is the volumetric flow rate through the turbomachine  is the density, T is temperature, p is pressure, Ro is the gas constant and is proportional to the universal gas constant divided by the molecular weight, and r is the pressure ratio. 

![](images/tmpfjnpspht.pdf-0035-05.png)

![](images/tmpfjnpspht.pdf-0036-00.png)

![](images/tmpfjnpspht.pdf-0036-01.png)

Turbomachine efficiency has been investigated extensively since the 1960’s. These analyses generally describe the results as a function of specific speed and specific diameter. These data have been collected and are frequently plotted as Ns-Ds diagrams which show the “average” efficiency that can be achieved as a function of specific speed and specific diameter.  For compressible flow the lines of constant “average” efficiency are shown as curves in Figure 4.1 for the compressor and in Figure 4.2 for the turbine (Balje, 1981).  Note that these curves are defined for machine Reynolds number > 2 x 10[6] and for single stage compressors and turbines. Also observe that the highest efficiencies that are achievable are slightly above 90% for the turbine and slight above 85% for the compressors.   The efficiency is defined as total-to-static enthalpy changes from inlet to outlet.  Also the specific speed must be near 0.7 for the turbine and just above 1.0 for the compressors.  Likewise the specific diameter for the most efficient machines is always near 3.   With careful attention to the details of flow, to vortex distribution and to blade loading, higher efficiencies can be achieved than reported in these Figures (Balje, 1981).  In this report we assume that a 2% improvement can be obtained using advanced design methods. 

![](images/tmpfjnpspht.pdf-0037-01.png)

**Figure 4.1  Specific Speed & Diameter (Ns Ds ) diagram for single stage turbines and expanders operating with compressible fluids.** 

![](images/tmpfjnpspht.pdf-0038-00.png)

**Figure 4.2:  Specific Speed & Diameter (Ns Ds ) diagram for single stage compressors (Balje, 1981).** 

Based on these figures it is seen that for optimum efficiency the specific speed and specific diameter must fall in a very narrow range, near 1 for the specific speed and near 3 for the specific diameter.  Because of these restrictions it means that the parameters such as flow rate, pressure drop, reactor power, etc. are also restricted via equations 5-1 through 5-7.  For example, because the specific speed for the turbine must be near 0.7-1.0, the values for the shaft speed, volumetric flow rate and individual stage temperature ratio are fixed according to equations 5-3 and 5-4 to this value.   Because the total volumetric flow rate through the turbomachinery is determined by the reactor power, it impacts the design of the turbomachinery.  Likewise so does pressure, molecular weight, shaft speed, and temperature rise through the reactor. 

The denominator of the specific speed and specific diameter equations always depends on the dynamic head of the stage.  The dynamic head can be reduced by increasing the number of stages, but clearly there are limits to the number of stages that any given compressor or turbine can have.  In this report we limit the turbine and compressor to axial machine with pressure ratios per stage (rotor-stator blade row) to fall between 1.04 – 1.2.  Through equations 5-1 and 5-2 this limit on stage pressure ratio impacts the temperature ratio and thus the adiabatic head does not change much. Because the denominator can not be changed substantially by design (the number of stages does impact the denominator but again it is relatively limited) we cannot make large changes to the specific speed. Thus the only way to strongly influence the specific speed is to change the shaft-speed (rpm), the gas density, or the molecular weight of the coolant. 

A close examination of Figure 4.1 and Figure 4.2  shows that the maximum efficiency that can be achieved falls in a very island specific speed to diameter values.   If the efficiency is plotted as a function of specific speed assuming that the specific diameter is selected to also provide the maximum efficiency then a simplified curve of efficiency versus specific speed can be obtained.  This curve is shown in Figure 4.3 along with values for a curve fit.  A similar curve is shown in Figure 4.4 for the turbine. 

![](images/tmpfjnpspht.pdf-0039-01.png)

**----- Start of picture text -----**<br>
1<br>0.903<br>effComp( vNs) 0.5<br>0<br>0<br>0.1 1 10<br>0.1 vNs 10<br>cfA  1.1406728399761311<br>cfB  0.013368209308721222<br>cfC   0.07286930901225997<br> 1<br>ln  Ns <br>effComp  Ns    cfA  cfB  Ns  ln  Ns   cfC    feffTM<br> Ns <br>**----- End of picture text -----**<br>

**Figure 4.3:  Compressor total-to-static efficiency shown as a function of specific speed assuming that the ideal specific diameter is also selected. The term feffTM=1.02 is used to increase the efficiency by 2% assuming that advanced turbomachinery design methods are used to develop the compressor.** 

![](images/tmpfjnpspht.pdf-0040-00.png)

**----- Start of picture text -----**<br>
1<br>0.93<br>effTurb( vNs) 0.5<br>0<br>0<br>0.1 1 10<br>0.1 vNs 10<br>etA  0.42726876<br>etB   0.53097712<br>etC  0.21150988<br>0.5<br>effTurb  Ns   eetA  etB  Ns  etC  ln  Ns  feffTM<br>**----- End of picture text -----**<br>

**Figure 4.4:  Turbine total-to-static efficiency shown as a function of specific speed assuming that the ideal specific diameter is also selected. The term feffTM=1.02 is used to increase the efficiency by 2% assuming that advanced turbomachinery design methods are used to develop the turbine.** 

These curves were used in our model to determine the efficiency of the turbine and compressor. 

## _**4.2 Effect of System Constraints on the Turbomachinery Design**_ 

The previous section provides the equations that quantitatively describe how the specific speed and specific diameter affect the design of the IHC Brayton cycle through relationships between the flow rate, power, gas type shaft diameter, pressure ratio, temperature and shaft speed.   As described in section 3.1.3, this report largely restricts the architecture layout and design to what are believed to be approaches that industry would consider representative. Therefore we have chosen a conservative design that restricts the shaft-speed to 60 Hz (3600 rpm) and a reactor with a thermal power of 600 MWth.  The power level was selected because it is thought to be at a sufficiently large level that economies of scale help lower the costs. 

## **4.2.1 Primary Circuit Temperature Constraints** 

We also have restricted the primary circuit inlet and outlet temperatures to 773 K and to 1190 K respectively. These values were selected based largely on material limitations of the reactor coolant vessel and the primary heat exchanger vessel.  The inlet temperature was selected to be low enough that it could be used to cool the pressure boundary.  For the three types of Brayton loops being examined the temperature rise across the reactor is based on materials restrictions and set to a temperature difference of about 417 K = 1190 K- 773 K. Because P=mdot*Cp*dT the mass flow rate is fixed once the gas type is chosen (Cp is unique for each gas type or gas 

mixture and depends only on molecular weight see equation 5-9 because the reactor power is set to 600 MWth.   In addition the temperature ratio of 1190 K / 773K also defines the pressure ratio via equation 5-1.  For an IHC CBC system (6c/3t) the pressure ratio per each turbine set or per each pair of compressors is fixed at about 3.4. The same pressure ratio is used for the simple and single interstaged cooling configuration. 

## **4.2.2 Grid Connection Constraints** 

Other constraints also apply.  For a grid connected power conversion unit the compressors and turbine all spin at 3600 rpm.  This means while the system is connected to the grid the flow rate through the reactor cannot be changed unless the system pressure is changed or flow is bypassed around the reactor.   With respect to turbomachinery design considerations this also means that the shaft speed is fixed in our “conservative” approach, therefore we cannot impact the specific speed by changing it.   If helium is chosen as the gas then the only remaining variables left that can impact the volumetric flow rate is the gas density by changing the system pressure.  However, even this value is limited due to material restrictions.  Generally the designs of gas cooled reactor keep the system pressure to lie below  1000 psi = 7 MPa for the high pressure leg of the system. This value is generally considered because it produces stresses in the ducting and pressure vessel structures that are thought to be near the upper creep limits of the materials. 

## **4.2.3 Pressure Ratio Constraints** 

For the IHC Brayton cycle the pressure ratio used for our standard 6c/3t design the pressure ratio in the turbine is approximately 3.4.  This large a pressure ratio is far from the ideal pressure ratio (which is closer to 2.0) but was selected because it provides the sufficiently low reactor or primary heat exchanger inlet temperature to satisfy material limitations.   For the 3 sets of turbines the overall pressure ratio is therefore close to 3.4[3] =39.  The consequence of such a large pressure ratio is that the lowest pressure stage will be very large as it will have a pressure near 24 psi which is only 75% above ambient pressure.  In effect the large total pressure ratio required by the IHC Brayton means that the low pressure turbines and compressor will be very large.  However a side benefit is that the system is very insensitive to pressure drops.  This will be discussed more in later paragraphs. 

## **4.2.4 Analysis Method used to Determine IHC Brayton cycle Behavior and Turbomachinery predict Constraints** 

In this report we have considered these limitations and restrictions for the design of the IHC Brayton cycle.  To address these issues a general program was written in MathCAD that solves for the cycle efficiency of IHC closed Brayton cycle systems using methods similar to those described in the earlier reports.  However in this report we have added modules to estimate the compressor and turbine efficiency based on the similarity analysis just described.  The result of this analysis determines the turbomachinery design information including the number of stages, the pressure ratios, the specific speeds, the specific and actual diameters, and the turbine or compressor efficiency. 

Three types of loops were examined.  The first is a simple recuperated Brayton cycle.  This cycle has one turbine and one compressor and is denoted as 1c/1t in many of the plots and tables that follow.  The second loop examined has one stage of intercooling.  In reality two 

coolers are used, one is called the pre-cooler or gas-chiller (or Waste heat exchanger), while the other is frequently called the inter-cooler. This second loop is denoted by 2c/1t in this report as there are two compressors and one turbine.  The last and third type of loop considered uses 6 compressors and 3 turbines and is denoted as 6c/3t.  This last loop has two inter-coolers and one precooler.  (In essence every compressor has one cooler though standard nomenclature and discussions of these systems use the phrase inter-cooler which refers to the number of coolers that follow the first compressor.)  In this analysis all heat exchangers and recuperators have effectiveness values of 95%. 

The IHC Mathcad analysis tool was used to determine the mass flow rates for the three gas Brayton loops under consideration.  We used this tool to determine the mass flow for both pure Helium coolant and for a 70/30 He/Ar mole fraction gas mixture.  The result of this analysis shows that the higher molecular weight gas mixture has substantially larger mass flow rates and thus will have higher volumetric flow rates as well.  This tends to increase volumetric flow rate in the specific speed equation (5-3) and therefore allows the designer to choose a molecular weight that provides the ideal specific speed and hence provides for optimum efficiency. 

## **4.2.5 Mass Flow Rate in the Brayton Cycles** 

Table 4-2 lists the calculated mass flow rate for a 600 MWth reactor for the three CBC gas Brayton loops being examined. There are a few important points to make from this table.  First for the 6c/3t IHC cycle the mass flow rate is approximately 1/3 of that for the simpler loops. This occurs because the simpler loops have a single heater where as the 6c/3t IHC loop has three primary heat exchangers.  Because the same temperature ratio (and pressure ratio) or temperature rise occurs in heat primary heater or re-heater , and it occurs three times in the 6c/3t IHC loop the mass flow rate is about 1/3 of  the flow that occurs in the single heated Brayton loops.  The second thing to observe is that the mass flow rate is substantially higher in the higher molecular weight gas mixture Brayton cycle than in the Helium Brayton cycle.  The higher flow rate increases both the turbine and compressor efficiencies (as shown in following paragraphs).  The higher molecular weight may make it easier to design the turbine and compressor because the mixed coolant has a molecular weight (14.87 gm/mole) that is closer to air (28.8 gm/mole) compared to helium which has a molecular weight of 4 gm/mole. 

**Table 4-1:  IHC gas Brayton cycle mass flow rates for the three Brayton loops, and for pure helium and for a 70/30 He/Ar gas mixture.** 

## _**4.3 Estimate of the Specific Speed and Efficiency of Turbomachinery for the Three IHC CBC Systems**_ 

The IHC Mathcad analysis tool (Mathsoft, 2006) was used for the three types of CBC Brayton loops to determine the specific speed and turbomachinery efficiency.  Initially this was done assuming that helium as the coolant.  The results of this analysis for the compressor and turbine are shown in the left columns of figure 5-1 and 5-2.  These tables show the “average” efficiency and specific speed for the three CBC loops.  For the compressor with helium as the coolant the specific speeds vary from 0.7 to 1 which is very close to the ideal range for the specific speed.  Because the specific speeds are near their ideal values the efficiencies are also high, on the order of 87-89 percent. However, if one looks at the turbine (see left hand column in Table 5-2) the specific speeds are low (on the order of 0.14-0.2 which results in relatively low efficiency (0.84-0.88).  As a reminder the earlier study used 0.93 for the efficiency of the turbine and 0.9 for the compressor. 

**Table 4-2:  Comparison of Average Compressor Efficiencies in three Gas Brayton Loops (6c/3t, 2c/1t, 1c/1t) for 100% He and a gas mixture of 70% He 30% Ar.** 

||**Compressors**|**Compressors**||||**Compressors**|**Compressors**|**Compressors**|||
|---|---|---|---|---|---|---|---|---|---|---|
||**100% He**|||||**70% He**|**30% Ar**||||
|||**Eff.s**|**N.s**|||||**Eff.s**|**N.s**||
||**6c/3t**|0.865451|0.748002|||**6c/3t**||0.897439|1.957043||
||**2c/1t**|0.894145|1.03175|||**2c/1t**||0.887504|2.665786||
||**1c/1t**|0.871997|0.725856|||**1c/1t**||0.902679|1.698008||
||||||||||||

**Table 4-3:  Comparison of Average Turbine Efficiencies in three Gas Brayton Loops (6c/3t, 2c/1t, 1c/1t) for 100% He and a gas mixture of 70% He 30% Ar.** 

||**Turbines**|||||**Turbines**||||
|---|---|---|---|---|---|---|---|---|---|
||**100% He**|||||**70% He 30% Ar**||||
|||**Eff.s**|**N.s**||||**Eff.s**|**N.s**||
||**6c/3t**|0.88936|0.266286|||**6c/3t**|0.922689|0.691412||
||**2c/1t**|0.853637|0.152212|||**2c/1t**|0.919347|0.386562||
||**1c/1t**|0.84612|0.140451|||**1c/1t**|0.910478|0.322691||
|||||||||||

All of the three CBC loops use high levels of recuperation.  For these systems a 300 MWe class power plant will have the turbine set produce about 600 MW of power and the compressor will consume about 300 MW of power resulting in a net power of 300 MWe.  The efficiency of the turbine is a very important parameter because the turbine power is twice as large as the compressor power.  Therefore, a 1% point decrease in turbine efficiency results in a 2% reduction in power and thus a 2% reduction in overall system efficiency.  Thus it is extremely important that the efficiency of the turbine be kept as high as possible.  To increase the turbine efficiency it will be necessary to increase the specific speed.  Lowering pressure helps but results in larger turbomachinery and greater expense.  The only two real options that are available to increase the speed are: 

1. to change the gas type by increasing the molecular weight, or 

2. to increase the rotational shaft speed of the turbo-compressor. 

For a grid connected synchronous generator the shaft speed of the turbine is fixed at 3600 rpm and thus cannot be changed without adding additional frequency conversion hardware. Therefore, in this report we have explored the option of increasing the molecular weight to achieve the higher efficiency.   Still the option of increasing the shaft speeds needs to be seriously considered and is indeed a technique that GA is using in their HTGR design approach (Baxi, 2006) 

The right hand column of Tables 5-1 and 5-2 shows the specific speed and efficiency for the three CBC loops with a coolant of 70% mole fraction Helium and 30% Argon. It is seen that for the 6c/3t IHC loop the average compressor efficiency was increased from 0.86 to 0.89, while the turbine efficiency also increased from 0.89 to 0.92.  As described earlier this 3% increase in turbine efficiency is expected to have a 6% overall efficiency improvement in the 6c/3t IHC Brayton cycle.  In fact our final analysis shows that simply by using the He/Ar gas mixture of 70/30 we get an increase in system efficiency from 48% to 52%.  However the change in molecular weight tends to decrease the thermal conductivity with respect to helium thus we will expect an mass increase in heat exchanger when a gas mixture is used. This mass increase is quantified in later sections of this report. 

## _**4.4 Summary Results from Similarity Analysis Applied to the Three ICH Brayton Cycles**_ 

The main conclusion obtained from this analysis of turbomachinery design constraints in the evaluation of gas Brayton systems is that in general the high efficiencies assumed in the simple thermodynamic cycle analysis can in fact be achieved based on similarity analysis of the turbomachinery.  However to achieve these high efficiencies the designer must change the coolant molecular weight for systems that are grid connected and take the heat exchanger mass penalty associated with lower gas thermal conductivity.  The other alternative is to increase the turbomachinery shaft speed and take the penalty associated with frequency conversion.  The first approach improves efficiency but results in a mass increase, the second approach has off setting characteristics with respect to efficiency increases because the higher speed improves the efficiency but this “advantage” may be reduced by the need to provide frequency conversion and the efficiency penalty associated with this.  In addition higher frequency turbomachinery will be smaller is size, thus will have lower costs, but again this is offset by the need to purchase frequency conversion hardware. 

Overall there are a number of benefits in changing the molecular weight in the fashion just mentioned for grid connected systems.  These include: 

- 1) The total cycle efficiency is greatly improved because the ideal specific speed can be obtained and high efficiency turbines and compressors can be developed. 

- 2) The gas molecular weight can be made closer to the molecular weight of air than when pure helium was used.  In fact if desired the molecular weight can be adjusted to match the molecular weight of air exactly while still keeping the specific speed at its optimum value.  Virtually all gas turbines are designed for using in air cycle combustion turbines and compressors.  Thus using a molecular weight that is close to air may help assure that the design is valid.  In addition increasing the molecular weight also provides more flexibility in the design as the number of stages used in each turbine or compressor set can be reduced.  In effect the higher volumetric flow rate term in the numerator of the 

specific speed equation permits a larger pressure ratio (and thus the temperature rise) per individual stage within each compressor set.   Typically the stage pressure ratio in an axial machine varies for 1.05 to 1.2, and the total number of stages is limited to around 20 or 30 at most.  ( In the analysis reported here the maximum number of stages allowed is 30.) 

- 3) The gas thermal conductivity is kept high because for the same molecular weight the He/Ar gas mixture will have a higher conductivity than a pure gas at the same molecular weight. 

- 4) The high density of the fluid and high velocity increases the density and thus the Reynolds number thus even though the thermal conductivity of the gas mixture is lower than for helium.  Its impact on the heat exchangers is more complex however as a 70/30 He/Ar gas mixtures has a greater heat transfer coefficient in the intercoolers but a smaller heat transfer coefficient in the gas heaters.  This will be illustrated in a series of tables that follow. 

- 5) Lastly, the gas mixture molecular weight can be easily changed to “dial” in the optimum efficiency. 

## **4.4.1 High Speed Turbomachinery and Frequency Conversion** 

As described earlier the alternative to changing the molecular weight is to change the shaft speed.  This very approach is now being considered by General Atomics for its Advanced High Temperature Reactor as they now intend to use a singe turbo-compressor alternator shaft that spins at 4400 rpm rather than 3600 rpm (ICAPP 2006).  It was unclear how they intend to convert the frequency.  To increase the shaft speed requires additional machinery. One approach that can be used is to use a gear reduction system that lets the turbo-compressor spin at one rate while the generator/alternator spins at another speed.  Gear driven transmission systems are efficient, typically they loose 1% per gear set (Barber-Nichols, 2006).  They are typically used in gas turbine systems in the power range from 5-50 MW (Mechanical Handbook, ) and can be designed to go higher but they will probably have a limited life because of metal-to-metal contact and thus we have not selected this as a via option. 

Another approach is to use some type of frequency conversion.  Frequency conversion can also be carried out by rotary equipment, typically a variable speed DC drive driving a synchronous generator.  but also by various other fixed speed motor/generator or compound motor/generator approaches.  Typical assumptions for efficiencies of motor generator sets are on the order of 97% - 98% per motor generator.  The resulting efficiency therefore would be on the order of 94%-96%.  As shown later in this report, the expected improvement in net electrical efficiency (due to higher shaft speeds) appears to only be 2-3%.  Thus even 4-6% penalty in efficiency caused by using a motor generator set appears to not be warranted as well. 

Today, modern IGBT (insulated gate bipolar transistor) devices overcome the limitations of transistor inverter systems and make possible fully solid state frequency conversion at up to MVA (mega watt) levels at economic prices for sufficiently long distant power transmission. Such systems make many new applications feasible including frequency conversion. Conversion efficiencies of up to 94% are possible. (Electronics online, 2001)  Based on this information we assume that it is prudent to assume an efficiency of about 94% for frequency 

conversion.  If this number holds up it represents a sizable penalty for systems that use spin faster than the grid frequency. 

Based largely on the above arguments, we have take the approach that to achieve the desired higher efficiencies offered by the IHC system it is best to adjust the gas mixture so that very high turbine and compressor efficiencies can be achieved.  As already shown a helium to argon mole fraction of 70 % helium and 30% argon makes the turbomachinery have specific speeds that are near the values that produce optimum efficiency and this is the approach taken in this report. In a sense by using gas mixtures it is possible to “dial” in the high turbomachinery efficiency. 

## _**4.5 Heat Exchanger Effects on Design**_ 

It is expected that much of the costs associated with the IHC Brayton loop will be due to the use of additional heat exchangers.  To determine this effect a first principles model for the heat exchanger was developed based on the NTU method.  Because the heat exchangers for the three cases being examined all transfer different amounts of heat and have different flow rates, gas types, inlet pressure and temperature we needed a model that was capable of predicting the consequences of these effects.  The model calculates the mass and size of the heat exchanger given the input temperature and pressures and gas types and desired fractional pressure drop for the heat exchanger.  Heat exchanger mass and size are used to determine costs of these components. 

## **4.5.1 Heat Exchanger Model Description** 

The heat exchanger model is based on the NTU method (Holman, xxx).  Counter flow parallel platelet or printed circuit like heat exchangers (of the style marketed by Heatric) is assumed. Corrections to the model are included to force the heat exchanger design  to produce specific surface areas (meter squared of heat transfer area per cubic meter of heat exchanger core volume) that match the publish values of Heatric (200-600 m[2] /m[3] ).  The wall thickness of each plate is forced to be 0.5 mm or greater depending on the pressure of the system.  The model uses a user specified NTU (number of heat transfer units) chosen to achieve the desired effectiveness (generally 0.90-0.95)  and determines the required heat transfer area based on the heat transfer coefficient using the formula h=Nu*k/dh where dh is the hydraulic diameter.  The formula the Nusselt number is presented which is applicable for laminar flow between flat plates. 

![](images/tmpfjnpspht.pdf-0046-06.png)

The heat transfer area is determined from Aht = NTU * mdot * Cp / h, where mdot is the mass flow rate, Cp is the gas specific heat at constant pressure, and h is the heat transfer coefficient. To be conservative we have used the heat transfer coefficient in the hot or low pressure leg as this 

The desired fractional pressure drop is input and the code determines a gas hydraulic diameter that provides this fractional pressure drop.  Typically we allow the fractional pressure drop to vary from 0.5% to 1.5% for each component.   The user specifies a flow length for the heat exchanger which is typically around 0.7 m and the code calculates the inlet flow frontal surface 

area which is specified by a recuperator height and width (Hxxx and Wxxx) where the subscripts indicate whether it is a recuperator (recup), gas chiller heat eXchanger (gcx), or a heater (htr). 

Pressure drop due to form losses that might occur due to area changes (especially abrupt expansions that might occur in the inlet and outlet plenums) are included by intrucing an input variable that represents the number of velocity heads evh and evc that could be seen by the fluid flow in both the hot and cold legs within the heat exchanger.  This variable is an input parameter but it is usually set to 4 for each leg. 

Three types of heat exchangers models were developed. One is for the gas cooler which assumes that water is the coolant in one leg and that He or Ar/He is the coolant in the other leg. A He to gas-mixture heat exchanger was developed for the primary circuit because the gas in the primary circuit is always assumed to be Helium a about 7 MPa.  The gas in the Brayton cycle may be helium or a gas mixture.  The last heat exchanger is the recuperator and it assumes that the coolant is the same in both legs. 

## **4.5.2 Example Results for the Heat Exchangers** 

The results of the exchanger model are illustrated here for the 6c/3t ICH Brayton loop configuration.  The results for both the coolers and heaters are shown, and the gas type was varied from the 70/30 mole percent He/Ar gas mixture to pure helium.  The He/Ar results are illustrated in  Table 4-5 and in Table 4-6.  The pure helium results are presented in Table 4-7 and in Table 4-8.  As shown the code output provides comprehensive list of output.  Table 5-3 identifies the names and definition of the more important input and output variables.  As describe above the input are the heat exchanger temperatures, pressure, fractional pressure drop desired, and the number of NTUs required to achieve the desired effectiveness. 

The intent of providing the tabular results for the IHC 6c/3t heat exchangers is to provide the reader with a sense of what the heat exchanger calculate and the general trends that are observed.  For these tables we used a constant fractional pressure drop of 0.5%.  The length of the heat exchanger was 0.7 m and the heat transfer area was chosen to provide a heat exchanger effectiveness of 95%.  Because the overall pressure ratio from the low pressure leg of the 6c/3t IHC Brayton cycle is almost a factor of 40 this means that there is a low pressure leg that is very large for both the heater and the gas cooler.  Likewise the recuperator has a low pressure leg which operates at near the lowest pressure in the system.  Because the fractional pressure drop was selected to be so low and the effectiveness is large the mass of these heat exchangers is la 

**Table 4-4:  Nomenclature used for the design of the heat exchangers.** 

**Table 4-5:  Gas cooler/chiller heat exchanger results for a 70/30 He/Ar gas mixture for a fractional dP of 1.5% with  a 95% effective heat exchangers and a 90 % effective recuperator.** 

**Table 4-6:  Gas heater/re-heater and recuperator heat exchanger results for a 70/30 He/Ar gas mixture for a 1.5% fractional dP with  a 95% effective heat exchangers and a 90 % effective recuperator..** 

**Table 4-7:  Gas cooler/chiller intercooler heat exchanger results for a pure Helium coolant.** 

## **Table 4-8:  :  Gas heater/re-heater and recuperator heat exchanger results with pure Helium and for a 0.5% fractional dP.** 

## **4.5.3 Heat Transfer in Mixed He/Ar gas Coolants** 

It was stated earlier that changing from pure helium to a 70/30 He/Ar gas mixture would impact the heat transfer coefficient.  This is illustrated in Table 4-9 and in Table 4-10 for the 6c/3t IHC Brayton loop configuration.  In these tables we compare the thermal conductivity, the Reynolds number, and the heat transfer coefficient that were predicted for the high and low temperature heat exchangers.  A range of numbers is given because this configuration of the Brayton loop has 3 re-heater heat exchangers and 6 pre-cooler or intercooler heat exchangers. The low and high values for the three heat exchangers are provided.  Based on the values in this table it is clear that for the gas heaters, even though the thermal conductivity is decreased in the He/Ar gas mixture, the heat transfer coefficient is about the same value as when helium was used.  This occurs because the density of the gas mixture is large thus the Reynolds numbers remain high as well.  The model for the heat exchanger is described elsewhere, but essentially it selects a hydraulic diameter, and a heat transfer area that satisfies the effectiveness assumptions (95%) and that keeps the pressure drop to less than 0.5% per heat exchanger.  Thus for these heaters there is indeed  no significant change in heat transfer coefficient but there does appear to be a slight increase.  This also corresponds to a slight decrease in mass for these heat exchangers compared to using pure helium. 

**Table 4-9:  Comparison of thermal conductivity, Reynolds number, and heat transfer coefficient in the primary circuit heat exchanger for the IHC 6c/3t loop with helium and he/ar 70/30 gas mixture.** 

||**k (w/m*K) @ 981 K**|**Re**|**h (W/m2-K)**|
|---|---|---|---|
|**Helium**|0.332|300-900|900- 2800|
|**Helium/Ar (70/30)**|0.190|1200– 2700|1200-2700|

The same comparison is made for the gas coolers, precoolers and intercoolers.  This time the trend is reversed as the heat transfer coefficient in the coolers decreases for He/Ar gas mixtures compared to those expected for pure helium. 

**Table 4-10:  Comparison of thermal conductivity, Reynolds number, and heat transfer coefficient in the gas leg of the gas precooler and intercoolers for the IHC 6c/3t loop with helium and He/Ar 70/30 gas mixture.** 

||**k (w/m*K) @ 300 K**|**Re**|**h (W/m2-K)**|
|---|---|---|---|
|**Helium**|0.154|3400- 16000|460-3200|
|**Helium/Ar (70/30)**|0.085|6300– 45000|270-1900|

For completeness we have also looked at the heat transfer in the recuperator.  For the recuperator the heat transfer model for the He/Ar gas mixture predicts a 25% increase in the heat transfer coefficient for the pure helium system. Thus it appears that the increase thermal resistance of the gas mixture does not strongly impact the heat transfer in the many stage IHC Brayton concept. 

## **4.5.4 Impact of Pressure on the Mass of the Heat Exchangers** 

The above analysis showed that the higher thermal resistance of the He/Ar gas mixture did not strongly affect the heat transfer coefficient for heat transfer.  However, our analysis shows that the gas pressure does strongly impact the size of the heat exchangers. This is described in more detail in Section 6.1. 

Overall the analysis shows that there is no strong pressure sensitivity for the two smaller gas Brayton cycle concepts because the pressure ratio for these two systems is 3.4.  However the total pressure ratio for the 6c/3t IHC system has a total pressure ratio of 39.  This large pressure ratio means that for the same high pressure of the loop (7 MPa) the low pressure and intermediate pressure heat exchangers are require large hydraulic diameters.  Because the heat transfer area is fixed by the high effectiveness of the recuperators, the larger hydraulic diameter flow passages for the low pressure coolant forces the size of the heat exchanger to be large.  A similar effect also occurs in the low pressure leg of the recuperator as this leg governs the size/mass of the recuperator. 

## **4.5.5  Primary Loop and Circulator Efficiency** 

The concept under evaluation for the multi-staged IHC Brayton cycle uses a primary loop. This was one of the limiting design constraints outlined in Section 3.1.   The analysis for the circulator used the similarity analysis approach to determine the efficiency of the circulator. The inlet temperature of the circulator is high (about 759 K) thus it is difficult to design the circulator to have a very high efficiency.  Still based on the analysis the specific speed of the circulator was about 2.1 which resulted in an efficiency of 89.7 %.   The power required to run the circulator is defined by 

![](images/tmpfjnpspht.pdf-0053-05.png)

Therefore the efficiency of the circulator is 

![](images/tmpfjnpspht.pdf-0053-07.png)

The pressure drop through the core for a 7 MPa Helium primary loop appears to be on the order of 1%, and the pressure drop in the primary heat exchanger is designed to be 0.5% and we estimate pressure drops in the ducting and turns to be about 0.2% thus the total primary loop pressure drop is about 1.7%.  This gives an efficiency for the circulator and primary loop of about 95.5 percent as shown in Figure 4.5 which shows the fractional power lost to the circulator and primary circuit.  In reality the losses are less than this 4.5% estimate because all the losses end up as additional heat in the primary loop.  Since about 40%- 50% of this will be converted back to electricity by the Brayton loop the average effective efficiency is about 2.5 – 3.0 %.  In our models we have used an effective efficiency in the primary loop of 97% which accounts for the circulator losses but adds the thermal heat/power to the primary gas of which 40-50% is converted back to electricity.   These results are summarized in Table 4-11. 

![](images/tmpfjnpspht.pdf-0054-00.png)

**----- Start of picture text -----**<br>
0.125<br>0.12<br>P circ  3  vr circ  0.1<br>P e<br>0.08<br>P circ(3  1.017)<br>P e<br>0.06<br>0.04<br>0.025<br>0.02<br>1 1.01 1.02 1.03 1.04 1.05<br>1.01 vr circ 1.05<br>**----- End of picture text -----**<br>

**Figure 4.5:  Fractional power lost to circulator inefficiency as a function of pressure drop in the core and primary heat exchanger.** 

**Table 4-11:  Performance characteristics of the primary helium gas loop.** 

## **5 Chapman Enskog Theory for Properties of Mixed Gases** 

It was shown previously that by using gas mixtures of inert gases it was possible to “dial in” the specific speed of the turbomachinery so that the system could operate near the highest efficiencies.  This approach has numerous benefits but the main one is that the turbomachinery speed can then be kept at 3600 rpm which is highly desirable for grid connected reactor driven gas Brayton loops. To use inert gas mixtures requires knowledge of the fundamental hydrodynamic properties of the mixed (or pure) gas such as gas heat capacity, gas thermal conductivity, viscosity, and Prandtl number.  These properties are required to estimate the heat transfer coefficient, mean flow velocities and pressure drops, Reynolds and Nusselt numbers. The calculation of these properties is described here. 

Mixed gases are often considered for use in special purpose applications because, for the same molecular weight, a mixed gas has a higher thermal conductivity than the pure gas.  When pure helium at high pressures is used in  power conversion system it tends to force the turbomachinery to be small (which may provide cost and size benefits) but it also forces the 

turbomachinery including the generator to operate at high shaft rotation speeds (> 3600 rpm for large 100’s MW terrestrial applications).  The high speed introduces loss as some form of frequency conversion must be applied.  This can be mechanical through a gear mechanism, but 300 MW transmission systems are a new technology that we wish to avoid.  Motor generor sets can be applied but this introduces losses typically 2% each for the motor and generator. Advanced power electronics with AC-DC-AC methods can also be applied but again inefficiencies are introduced (probably on the order of 2-3 %. 

We use the Chapman-Enskog theory to determine the transport properties for the low density monatomic gases helium and Argon.  These properties are mixed according to a method by Mason and Saxena (1957) that is an approximation to a more accurate method developed by Hirschfelder (1954).  These transport properties are described in Bird-Stewart-&-Lightfoot (Bird 1960). 

Given the molecular weight of the ideal gases, the mole fraction of the gas mixture, the universal gas constant, and the ratio of the specific heats (constant pressure to constant volume)  , one can then determine the specific heat, molecular weight, speed-of-sound, density, and specific heat ratio for the gas mixture.  These equations for a 90% helium fraction are described below. 

## _**5.1 Gas Material Properties for Ideal and Monatomic Gases**_ 

The gas properties for the molecular weight (MW), and specific heat ratio (  of pure helium and Arnon as well as their mixed values are listed below. 

## **Table 5-1:  Ideal gas properties for helium and argon and their mixture at 70.0 a% helium.** 

|**helium.**|||
|---|---|---|
|Argon Molecular Weight MWAr|MWAr=  39.948 gm/mole|**5-1a**|
|Helium Molecular Weight MWHe|MWHe= 4 gm/mole|**b**|
|Ratio of Cp/ Cvfor  He|He|**c**|
|Ratio of Cp/Cvfor Ar|Ar|**d**|
|Argon Mole Fraction|fAr=  0.30,   30.0 a%|**e**|
|Helium Mole Fraction|fHe= 1- fAr= 0.700 , 70.0 a%|**f**|
|Average = Cp/Cv ratio|fArArfAr)Ar|**g**|
|Average Molecular Weight|MWo= 14.798  gm/mole|**h**|
|Gas Constant for mixed gas property|Ro= Rugc/ MWo= 562.35J/kg-K|**i**|

With these properties for the He and Ar mixture properties the equations for the density, the speed-of-sound, and the specific heat are: 

## **Table 5-2:  Density, speed of sound, and heat capacity equations for ideal gases with the heat capacity of  He/Ar at 70.0 a% listed.** 

Density equation for an Ideal Gas 

Speed of sound equation for a gas mixture at temperature T Heat capacity equation for an ideal gas 

![](images/tmpfjnpspht.pdf-0056-03.png)

Heat capacity for 70.0 a% He mixture Cp = 1414. J/kg-K 

**d** 

## _**5.2 Chapman Equation for Cp, k, and Viscosity for Gases**_ 

The Lennard-Jones potentials along with the molecular theory of gases and liquids can be used to predict the viscosity and the conductivity of gases at low densities. The Lennard-Jones potential values used are from Hirschfelder (1954).  A simple and concise summary of this theory is in Bird (1960, pp 744-746).  The Lennard-Jones potentials for He and Ar are given below. 

Lennard-Jones Parameters for He 

Lennard-Jones Parameters for Ar 

![](images/tmpfjnpspht.pdf-0056-10.png)

This data is used with a transport theory prediction curve  (T) to obtain the viscosity and conductivity at low densities for monatomic gases as a function of temperature and gas mixture. (Hirschfelder, 1954). 

![](images/tmpfjnpspht.pdf-0056-12.png)

Given this equation, the viscosity for a low density monatomic gas (Bird, Stewart, and Lightfoot, 1969) is defined by 

![](images/tmpfjnpspht.pdf-0056-14.png)

For example, the viscosity for helium at 300 K and 1000 K is 1.979 x 10[-5 ] Pa-s and 4.306 x 10 -5 Pa-s respectively.  Similarly, the conductivity for a low density monatomic gas, with  > 1.63,  is defined by (ibid, pg 255): 

![](images/tmpfjnpspht.pdf-0057-00.png)

At 300 K and 1000 K the gas conductivity for helium is 0.154 and 0.336 W/m-K. 

## _**5.3 Mixture Rules for the He/Ar gas mixture**_ 

The semi-empirical formula from Wilke (1950) is used to determine the mixed gas properties for thermal conductivity and for viscosity.  (See also Bird, 1960, pp 24 and 258.)  These rules are listed below. 

![](images/tmpfjnpspht.pdf-0057-04.png)

![](images/tmpfjnpspht.pdf-0057-05.png)

![](images/tmpfjnpspht.pdf-0057-06.png)

![](images/tmpfjnpspht.pdf-0057-07.png)

![](images/tmpfjnpspht.pdf-0057-08.png)

The Prandtl number for the He/Ar gas mixture is now defined as 

![](images/tmpfjnpspht.pdf-0057-10.png)

where the mixed properties for Cp, viscosity and conductivity are used. 

These equations were programmed in the programming environments Mathcad[TM] , Excel[TM] , MatLab[TM,] and Simulink[TM ] to specify the state properties of the closed Brayton cycle system described in the previous section.  In addition the complete theory (Hirschfield, 1954) was programmed into Mathcad and compared with the more simple theory described here (Wilke 1950).  An internal SNL memo is available on the complete theory. The more complete theory was developed because the Prandtl numbers for the individual gases are very similar, but the 

Prandtl number for the mixture is much lower than the individual values.  Because the Prandtl number plays an important role in the heat transfer coefficient from the pin to the gas coolant, we felt that it was important to verify this behavior especially for gas mixtures with very different molecular weights. We observed very little differences between the more complete theory and the condensed semi-empirical theory. 

Figure 5.1 shows the results of the Chapman-Enskog theory predictions for the thermal conductivity, viscosity and Prandtl number for various Helium Argon gas mixtures. The results provide some insight to the design of reactors and small gas-dynamic power conversions systems.  First, both the conductivity and viscosity show the standard square-root of temperature dependence that is expected.  For increasing helium content the gas conductivity increases monotonically, however, for the viscosity the values remains relatively constant or increase slightly, but then the viscosity drops dramatically at high helium fractions (> 80 a%). Because leak rates will be greater for helium than for Argon, there will be a tendency for the mole fraction of helium to decrease over the life of the system.  Depending on the leak rates, this could result in increased viscosity and lower conductivities.  Such changes are not likely to seriously affect the design, but they do introduce expected deviations that will have to be accommodated by providing adequate design margin. 

As mention earlier the Prandtl number shows unexpected behavior with respect to changes in helium fraction.  Both helium and Arnon have Prandtl numbers near 0.7, however the mixture shows a very reduced value (Pr = 0.4) at mixtures containing about 60 a% helium. 

Equation 4-4c provides the constant pressure heat capacity (Cp) as a function of Helium mole fraction which is inversely proportional to molecular weight.   Note that because the model assumes that the gas mixture is an ideal gas, that there is no temperature dependence for the heat capacity. 

![](images/tmpfjnpspht.pdf-0059-00.png)

**----- Start of picture text -----**<br>
0.4 0.4<br>kfmix( vT  .9) 0.3 kfmix  1200  K  vfHe  0.3<br>kfmix( vT  .8) kfmix  1000  K  vfHe <br>0.2 0.2<br>kfmix( vT  .7) kfmix  800  K  vfHe <br>kfmix( vT  .6) 0.1 kfmix  600  K  vfHe  0.1<br>0 0<br>0 500 1000 1500 0 0.5 1<br>vT vfHe<br>K<br> fmix( vT  0.9)5 [] 10 5  fmix  1200  K  vfHe <br>5<br>5 [] 10<br> fmix( vT  0.8)  fmix  1000  K  vfHe <br>5<br>4 [] 10<br> fmix( vT  0.7)  fmix  800  K  vfHe <br>5<br>4 [] 10<br> fmix( vT  0.6) 5  fmix  600  K  vfHe <br>3 [] 10<br>5 5<br>2 [] 10 3 [] 10<br>0 500 1000 1500 0 0.5 1<br>vT vfHe<br>0.7 0.7<br>Prfmix( vT  1) 0.6 Prfmix  1200  K  vfHe  0.6<br>Prfmix( vT  .9) Prfmix  1000  K  vfHe <br>0.5 0.5<br>Prfmix( vT  .8) Prfmix  800  K  vfHe <br>Prfmix( vT  .7) 0.4 Prfmix  600  K  vfHe  0.4<br>0.3 0.3<br>0 500 1000 1500 0 0.5 1<br>vT vfHe<br>**----- End of picture text -----**<br>

**Figure 5.1:  Mixed gas thermal conductivity, viscosity, and Prandtl number versus temperature or as a function of helium mole fraction in a Helium Argon gas mixture.** 

## **6 Performance and Sizing Estimates for Three IHC Brayton Cycles** 

This section of the report presents the sizing and mass estimate results based on the model described above.  Six systems are compared.  The three types of IHC Brayton cycles were examined for two working fluids.  One working fluid consisted of a 70/30 mix of helium andargon while the other was pure helium.  As described above the gas mixture was selected because it allowed the turbomachinery to operate efficiency at 3600 rpm or 60 Hz.  However for comparison purposes the same cycle was operated with Helium at 3600 rpm even though the turbine and compressor efficiencies were operating at specific speeds that cannot did not produce optimum cycle efficiency.  Nevertheless the results indicate that the reduction in cycle efficiency is only 2 -3 % . 

Overall the results show that the “ideal” net electric efficiencies of near 50.4% can be achieved by using the 6c/3t IHC with a 70/30 mole fraction of a helium/argon gas mixture.  When helium is used as the coolant the efficiency reduces to 48.2%.  The use of the gas mixture however does require additional mass for the heat exchangers and larger turbomachinery. These results are illustrated in Table 6-1 through Table 6-3. 

Table 6-1 summarizes and compares the mass of the heat exchangers for the three cycles and for the two gases.  This table provides the net electrical cycle efficiency and the mass estimates for all the heat exchangers including heaters, re-heaters, pre-coolers, inter-coolers, and the recuperator.  For the multiple re-heated and intercooled (6c/3t) configuration there are a total of 10 heat exchangers, while the simpler Brayton cycles have only 3 or 4 heat exchangers.  Even though the heat transferred in the 6c/3t IHC heat exchangers is less than in the simpler systems the heat exchangers can get very large because the pressures in the low pressure portion of the loop is very low.  The net result of this is that the mass of the heat exchangers increases as the pressure is lowered.  The net effect is that one cannot scale by power, but one must base the heat exchanger mass estimate on a design that accounts for heat transfer, pressure drop, heat transfer are and material strengths.  This is the approach that we took in this report and was the method described above in Section Heat Exchanger Effects on Design4.5.  Table 6-3 summarizes the results and compares the size of the turbomachinery for the three cases He/Ar and the three pure helium cases. 

When comparing net electrical efficiency produced in the He/Ar systems to pure helium, we see that in all cases the efficiencies of the pure Helium system are reduced by about two percentage points for all three types of Brayton cycles.  However one also sees that the mass of the heat exchangers (heaters, coolers and recuperators) for the pure helium Brayton cycle is about 30% less than for the gas mixture.   Likewise the turbine and compressor wheels are reduced in size by about 30% as well. As described the heat exchanger model includes conductivity effects, Reynolds numbers, viscosity, gas density and pressure, heat transfer area as well as inlet and outlet losses.  In the analysis presented here we made an effort to design systems that had small heat exchanger masses.  To accomplish this we had to increase the pressure drop in the recuperator and the heat exchangers and lower the recuperator effectiveness from 0.95 to 0.9.  For the He/Ar mixture the flow path length was reduced to 0.5 meter while it was kept at 0.7 m for the pure helium systems.  The pressure drop used in the heat exchanger model is listed in Table 6-1.  Note that for both gas types the recuperator design allowed for a pressure drop of 2.5% and the heaters and coolers had pressure drops of 1.5%. 

To be sure lower pressure drop heat exchangers are possible but the mass of the low pressure drop systems is much larger, based on our models. 

When comparing among the various cycles for the same gas we see in Table 6-1 that the multiple staged IHC cycle (6c/3t) has heat exchanger mass estimates that are about 3 times those of the two simpler Brayton cycles but produces a higher net electrical efficiency of 50.4%.  This net electrical efficiency is 5-7% higher than can be achieved in the simpler systems (45.8% and 42.8%).   The primary reason that the heat exchanger mass is higher in the 6c/3t IHC system (see Table 6-4) is because the pressure in the intermediate and low pressure portion of the loop are so low.  The lower pressure means lower gas density, which means larger hydraulic diameter which in turn means a more massive heat exchanger.  For the same reasons the turbomachinery dimensions are a factor of two larger as well (see Table 6-3).  Thus we see that the additional efficiency is achieved at a fairly high apparent costs based solely on mass and diameter of the turbo machinery. 

Our initial our initial models we have assumed  that all the turbomachinery compressor and turbine sets used the same number of stages which are summarized in Table 6-2. 

**Table 6-1:  Summary performance estimates giving the electrical efficiency and the total heat exchanger mass used in He/Ar gas mixture and pure Helium Brayton Cycles for the three concepts.** 

**Table 6-2:  Number of compressor and turbine stages for the three concepts.  Cost estimates will be proportional to the number of stages for each concept.  The same number of blade row set (stator + rotor) is used for the He/Ar and the pure helium gas type.** 

**Table 6-3:  Diameter of compressor and turbine wheels.  Estimates were made for the first wheel pair (rotor/stator) for the compressor and the last wheel pair (stator/rotor) for the turbines.** 

**Table 6-4:  Inlet and Outlet pressures for the compressors and turbines.  Same values are used for He/Ar coolant and the Helium coolant.  Pressures are in kPa.** 

![](images/tmpfjnpspht.pdf-0063-00.png)

## **Figure 6.1:  Conceptual layout of 6c/3t interstage heating and cooling Brayton Cycle.  The dimensions are approximately 48 m x 44 m** 

## _**6.1 Tables of Heat Exchanger Mass Comparisons showing the Strong Pressure Sensitivity**_ 

Because the pressure changes after each compressor or turbine set the mass of the heat exchangers varies along the flow path.  For the multiple 6c/3t IHC system the pressure ratio is almost 40-1. Therefore, the low pressure leg is only 78% above atmospheric pressure even though the high pressure leg is at 6894 kPa or about 1000 psi (see Table 6-4).  This means the for the cold leg of the 6c/3t IHC loop the gas pressure increases six times along the flow path and the cooler mass decreases as the pressure increases.  These step decreases are shown in Table 6-5 which provides a bar chart of the mass of the individual heat exchangers in the 6c/3t IHC system. The height of the blue bars shows the gas cooler mass.  Similarly the mass of the heaters increases as the gas flows through the three heaters (red bars in Table 6-5).  The recuperator size is determined by the low pressure leg after the last turbine.  Therefore it also has a large mass.  In the design used here its mass is very close to the mass of the low pressure heater. The top figure shows the heat exchanger mass for the He/Ag gas mixture and the bottom figures shows the same results but for pure helium.  The remaining figures in this section (Table 6-5, Table 6-6, and Table 6-7) show the individual heat exchanger mass for both He/Ar and pure helium for each of the three IHC systems. 

## **Table 6-5:  Comparison of the heater and cooler heat exchanger mass in the 6c/3t IHC Brayton cycle for a He/Ar gas mixture of 70/30 mole percent (top image) and for pure helium (bottom image).** 

![](images/tmpfjnpspht.pdf-0064-01.png)

**----- Start of picture text -----**<br>
Mass Estimates of Intercoolers, Reheaters and Recuperator<br>HeAr 70/30 gas mixture for the 6c/3t IHC CBC configuration<br>180000<br>160000 Cooler A<br>140000 Recuperator<br>Heater C<br>120000<br>100000 Cooler B<br>Gas Chillers<br>ReHeaters + Recuperator<br>80000<br>60000 Cooler C<br>Heater B<br>40000 Cooler D<br>Heater A Cooler E<br>20000<br>Cooler F<br>0<br>1 2 3 4 5 6<br>Heat Exhanger<br>Mass Estimates of Intercoolers, Reheaters and Recuperator<br>He gas for the 6c/3t IHC CBC configuration<br>100000<br>Heater C<br>90000 Recuperator<br>Cooler A<br>80000<br>70000<br>60000<br>Cooler B Gas Chillers<br>50000<br>ReHeaters + Recuperator<br>40000 Heater B<br>Cooler C<br>30000 Heater A<br>20000 Cooler D<br>Cooler E<br>10000 Cooler F<br>0<br>1 2 3 4 5 6<br>Heat Exhanger<br>Mass (kg)<br>Mass (kg)<br>**----- End of picture text -----**<br>

**Table 6-6:  Comparison of the heater and cooler heat exchanger mass in the 2c/1t Brayton cycle for a He/Ar gas mixture of 70/30 mole percent (top image) and for pure helium (bottom image).  The lower pressure legs have higher heat exchanger mass.** 

![](images/tmpfjnpspht.pdf-0065-01.png)

**----- Start of picture text -----**<br>
Single Intercooler (2c/1t) Heat Exchanger Mass Estimates<br>80000<br>70000<br>60000<br>50000<br>m.gcxCore<br>40000 m.htr_core<br>RecupS<br>30000<br>20000<br>10000<br>0<br>A_S B_S<br>Cooler, Heater or Recuperator<br>He/Ar<br>**----- End of picture text -----**<br>

![](images/tmpfjnpspht.pdf-0065-02.png)

**----- Start of picture text -----**<br>
Single Intercooler (2c/1t) Heat Exchanger Mass Estimates<br>50000<br>45000<br>40000<br>35000<br>30000<br>m.gcxCore<br>25000<br>m.htr_core<br>20000 RecupS<br>15000<br>10000<br>5000<br>0<br>A_S B_S<br>Cooler, Heater or Recuperator<br>Pure He<br>**----- End of picture text -----**<br>

**Table 6-7:  Comparison of the heater and cooler heat exchanger mass in the 1c/1t (simple recuperated) Brayton cycle for a He/Ar gas mixture of 70/30 mole percent (top image) and for pure helium (bottom image).  Note that the lower pressure legs of the loop have higher heat exchanger mass.** 

![](images/tmpfjnpspht.pdf-0066-01.png)

**----- Start of picture text -----**<br>
Simple Recuperated Heat Exchanger<br>Mass Estimates<br>80000<br>70000<br>60000<br>50000<br>m.gcxCore<br>40000 m.htr_core<br>m.htr_core<br>30000<br>20000<br>10000<br>0<br>Z<br>Cooler, Heater, Recuperator<br>He/Ar<br>Simple Recuperated Heat Exchanger<br>Mass Estimates<br>50000<br>45000<br>40000<br>35000<br>30000 m.gcxCore<br>25000 m.htr_core<br>20000 RecupZ<br>15000<br>10000<br>5000<br>0<br>Z<br>Cooler, Heater, Recuperator<br>He<br>Heat Exchanger Mass (kg)<br>Heat Exchanger Mass (kg)<br>**----- End of picture text -----**<br>

## _**6.2 Performance for the 1c/1t Simple Recuperated Brayton Cycle**_ 

The performance estimates for the simple 1c/1t recuperated Brayton cycle were calculated using the similarity scaling models for the turbomachinery and the heat exchanger model described earlier.  The code is written in Mathcad and is called SNL-CBC-IHC-Solver and it currently determines the design of the three IHC Brayton cycles.  The code transfers its results directly to an excel file which from the comparative plots and tables are generated and the cost analysis is performed (see section 7). 

Figure 6.2 shows a schematic loop diagram of the simple 1c/1t recuperated Brayton cycle. This figure shows the nomenclature used to identify locations at the various stations around the loop.  Station 1 always starts at the compressor inlet.  Station 2 is the compressor outlet, and these values increase around the loop.  When multiple compressors exist, the first compressor along the flow path is labeled with a subscript a or A, followed by b or B. 

The analysis has been performed for both He/Ar gas mixtures and for pure helium as the working fluid.  The code is sufficiently general that the pressures can be changed, as can the gas mixtures, turbomachinery speeds etc.  There are too many variables to address all combinations, and therefore the results presented are not expected to represent a minimum cost system.  The design sufficiently robust design to produce high efficiency but simple enough to be practical.  The maximum pressure has been set at 7 MPa, though smaller system masses could be obtained by simply increasing the system pressure. 

![](images/tmpfjnpspht.pdf-0067-04.png)

**----- Start of picture text -----**<br>
Reactor<br>Trx_in Tsrc<br>Helium<br>3 HTRA<br>Circulator<br>4 Generator<br>70 % Helium<br>30 % /Argon<br>T A C A<br>1<br>5 2<br>Gas Chiller<br>GCXA HX<br>Water Tsnk<br>3 6<br>Recup<br>**----- End of picture text -----**<br>

**Figure 6.2:  Simple recuperator Closed Brayton Cycle (CBC) having one turbine and one compressor.  (1c/1t CBC configuration).** 

## **6.2.1 Helium Argon Gas Mixture Configuration** 

The SNL-CBC-IHC-Solver code first determines a cycle analysis to determine all the gas station temperatures and the cycle efficiency.  This cycle solver uses assumed guess values for the efficiencies of the turbines and compressors.  Once this cycle is solved then given the requested power level, the mass flow is determined and the similarity analysis is performed to determine the size, number of stages, and efficiency of the turbomachinery.  The cycle analysis must then be repeated using the newly calculated values for the compressor and turbine efficiencies. 

Using this approach we have collected the predicted data for the simple recuperated 1c/1t Brayton cycle in 

Table 6-9.  The left hand column shows the gas temperatures, number of turbines and compressor sets assumed, the electrical power generated, the cycle efficiency, the electrical efficiency and the assumed effectiveness of the generator and circulator. The results shown in 

Table 6-9 are for the He/Ar gas mixture, but tables for the pure helium loop are available also but not presented here.  The right hand column provides the turbomachinery design.  The nomenclature for the variables is provided in Table 6-8. 

The cycle analysis shows that the mass flow rate is 1023 kg/s and the total net electrical efficiency is 42.8%.  For the turbomachinery, the simple recuperated 1c/1t Brayton cycle the specific speed of the turbine is (N.tZ=0.678), the turbine efficiency is (teffZ=0.856) and the turbine blade diameter is 1.61 m.  Note that the inlet pressure is 2108 kPa and the outlet pressure is 6894 kPa.  Because the pressure is high it keeps the turbomachinery dimension small compared to the 6c/3t system.  For this system 30 stages of turbine blade row sets were assumed.  (This is larger than we would like. To decrease the number of stages the Argon gas fraction needs to be increased.) 

**Table 6-8:  Definition of the turbomachinery variables.  Same nomenclature is used for the other CBC systems, but subscripts are used to identify the specific compressor or turbine.** 

**Table 6-9:  Results of Cycle and turbomachinery analysis for the He/Ar simple recuperated.  Cycle efficiency and gas temperatures are provided in the cycle analsys results.  The turbine and compressor efficiencies and size estimates are given for the turbomachinery design estimates.  Cycle efficiency is 42.8%, compressor efficiency was estimated to be 90% and the turbine efficiency for 10 stages was estimated to be 86%, however by reducing the number of stages the turbine efficiency can be increased to the 91% value used in the cycle analysis.** 

||**Cycle Analysis**|**1c/1t**|**1c/1t**||||**Turbomachinery Dsgn Z**|**Turbomachinery Dsgn Z**||
|---|---|---|---|---|---|---|---|---|---|
||T.src * (K)|||1190|||nZ|10||
||T.rej* (K)|||300|||r.cZ|1.125783231||
||f.dp|||0.05|||p.1Z (kPa)|2108.488469||
||n.turb|||1|||p.2 (kPa)|6894.757293||
||n.comp|||1|||r.zc|3.27||
||r.ce|||3.27|||p.4Z (kPa)|6894.757293||
||e.x|||0.9|||N.sZ|1.974242527||
||eta.c|||0.901|||lb.Z (m)|0.035834116||
||eta.t|||0.912|||D.z (m)|2.29206188||
|||1||1|||q.adZ|0.114029305||
||T.z1|||312|||N.tZ|0.678454653||
||T.z2|||526.2747815|||D.tZ|1.612733108||
||T.z3|||762.6803532|||q.ad_tZ|1.742563016||
||T.z4|||1190|||teffZ|0.856306625||
||T.z5|||788.9476389|||r.tz|1.041635959||
||T.z6|||552.5420672|||effCompZ|0.899852813||
||P.eZ|||311681428.6|||0|0||
||P.th/eff.circ (W)|||617919670.4|||0|0||
||eff.cycl|||0.437091018|||0|0||
|||1||1|||0|0||
|||1||1||||||
||eff.gen|||0.98||||||
||eff.circ|||0.971||||||
||NTU|||19||||||
||mdot.z|||1023.425389||||||
||eta.Z.electric|||0.428349198||||||
|||||||||||

The thermal hydraulic performance and the mass estimates for the heat exchangers for the 1c/1t simple recuperated He/Ar Brayton cycle is listed in Table 6-10.  The gas chillers information is on the left column, and the right column gives the heater and recuperator information.  The nomenclature for these tables was described in Table 4-4. 

**Table 6-10:  Thermal hydraulic performance details for the simple recuperated gas cooler, recuperator and heater with a 70/30 He/Argon gas mixture.** 

||**Chillers**|Z|||**Heaters**|**Z 1c/1c**|**RecupZ**||
|---|---|---|---|---|---|---|---|---|
||**H.recup**|1.326903604|||**H.gcxC**|4.46827534|2.829338059||
||**n.ch**|298.1699047|||**n.ch**|2368.520272|1055.427383||
||**f.dp**|0.015000005|||**f.dp**|0.014999969|0.015000004||
||**A.ht**|2782.919111|||**A.ht**|5526.547302|5746.215752||
||**Re**|43465.05682|||**Re**|5014.959928|6252.60327||
||**h1**|1889.575694|||**h1**|4976.527001|2267.186445||
||**v.h**|24.95934511|||**v.h**|22.98387346|26.01121321||
||**dp.h**|31627.33806|||**dp.h**|27408.93544|28922.50273||
||**dp.c**|92.12798429|||**dp.c**|103421.1456|8844.80206||
||**m.gcxTot**|22727836.3|||**m.htr_tot**|3102076.688|15125356.03||
||**m.gcxCore**|53054.10209|||**m.htr_core**|57949.94026|75517.48258||
||**m.gcx_pv**|22674782.19|||**m.htr_pv**|3044126.748|15049838.55||
||**t.wall_gcx**|0.0005|||**t.wall_htr**|0.0005|0.0005||
||**r.pv_gcx**|22.06173157|||**r.pv_htr**|5.515432893|12.86934342||
||**t.pv_gcx**|0.436460444|||**t.pv_htr**|0.891410482|0.841344236||
||**A2V.gcxCore**|438.5184716|||**A2V.htrCore**|797.2732196|636.1224189||
||**d.h_gcx**|0.003447119|||**d.htr**|0.000887792|0||
||**W.gcx**|12|||**W.htr**|3|0||
||**L.gcx**|0|||**L.htr**|0.7|0||
||**e.vh**|4.04|||**ev.h**|4.04|0||
||**e.vc**|4.04|||**ev.c**|4.04|0||
||**NTU**|3.632772671|||**NTU**|19|0||
|Cooler||||Heater and Recuperator|||||

## _**6.3 Performance for the 2c/1t Single Intercooler Gas Brayton Cycle**_ 

The performance estimates for the simple 2c/1t single intercooler recuperated Brayton cycle is provided in this section.  These results were developed using the similarity scaling models for the turbomachinery and the heat exchanger model describe earlier.    Figure 6.3 shows a schematic loop diagram of the simple 2c/1t recuperated Brayton cycle.  This figure shows the nomenclature used to identify locations at the various stations around the loop.  Station 1 always starts at the compressor inlet.  Station 2 is the compressor outlet, and these values increase around the loop.  The first compressor along the flow path is labeled with a subscript a or A, followed by b or B.  This proposed loop uses a pure helium primary loop and a separate gas in the Brayton cycle. 

![](images/tmpfjnpspht.pdf-0071-00.png)

**----- Start of picture text -----**<br>
Reactor<br>Trx_in Tsrc<br>Helium<br>HTRA<br>Circulator<br>Synchronous<br>Generator<br>70 % Helium<br>30 % /Argon<br>T A C B C A<br>Gas Chiller<br>GCXB GCXA HX<br>Water Tsnk<br>Recup<br>Helium / Argon<br>1<br>**----- End of picture text -----**<br>

**Figure 6.3:  Single intercooler Closed Brayton Cycle (CBC) having one turbine and two compressors.  In this report it is identified as the 2c/1t CBC configuration or sometime as the system having one stage of intercooling, even though two coolers are used.** 

## **6.3.1 Helium Argon Gas Mixture Configuration** 

The tables of the cycle performance and the turbomachinery design for the 2c/1t Brayton loop is provided in Table 6-11.  The same nomenclature as described earlier is used here.  Note that for the 2c/1t system the net electrical efficiency is 45.8%, though the cycle analysis results in 48.2%.   This reduction in efficiency is due largely to the inefficiency of the generator and the circulator which had efficiencies of 98% and 97.1% respectively. 

**Table 6-11:  :  Results of Cycle and turbomachinery analysis for the He/Ar IHC 2c/1t system with one intercooler.  Cycle efficiency is 45.8%, compressor efficiency was estimated to be 89.7% and the turbine efficiency was estimated to be 92.9%.** 

The thermal hydraulic performance and the mass estimates for the heat exchangers for the 2c/1t He/Ar Brayton cycle is listed in Table 6-12.  The gas chillers information is on the left column, and the right column gives the heater and recuperator information.  As before, the nomenclature for these tables was described in Table 4-4. 

**Table 6-12:  Thermal hydraulic performance details for the IHC Brayton cycle with a single intercooler (2c/1t).  The cooler data is for the two coolers and the heater data is for the heater and the recuperator.** 

||**Chillers**|A_S|B_S|||**Heaters**|**S 1c/1t**|**RecupS**||
|---|---|---|---|---|---|---|---|---|---|
||**H.recup**|1.370013524|0.797776195|||**H.gcxC**|4.479155668|2.832685579||
||**n.ch**|304.8229075|205.8935698|||**n.ch**|2374.28977|1075.400825||
||**f.dp**|0.015000013|0.015000016|||**f.dp**|0.014999969|0.01500034||
||**A.ht**|2845.013804|1921.673318|||**A.ht**|5540.009463|5854.960048||
||**Re**|42882.5112|63631.83047|||**Re**|5014.965452|6625.618404||
||**h1**|1852.83641|2743.101604|||**h1**|4976.526568|2230.497835||
||**v.h**|24.91793484|24.24994588|||**v.h**|22.92803554|24.52798685||
||**dp.h**|30418.07322|56088.16633|||**dp.h**|27275.89523|27996.86272||
||**dp.c**|85.50609097|291.5588751|||**dp.c**|103421.1456|8234.37139||
||**m.gcxTot**|21856858.17|40235736.74|||**m.htr_tot**|3102217.791|15031893.95||
||**m.gcxCore**|54659.06803|32935.91954|||**m.htr_core**|58091.04242|76032.28031||
||**m.gcx_pv**|21802199.1|40202800.82|||**m.htr_pv**|3044126.748|14955861.67||
||**t.wall_gcx**|0.0005|0.0005|||**t.wall_htr**|0.0005|0.0005||
||**r.pv_gcx**|22.06173157|22.06173157|||**r.pv_htr**|5.515432893|12.86934342||
||**t.pv_gcx**|0.419666834|0.773759939|||**t.pv_htr**|0.891410482|0.836095075||
||**A2V.gcxCore**|435.1394244|487.7710768|||**A2V.htrCore**|797.2740234|643.772169||
||**d.h_gcx**|0.003491483|0|||**d.htr**|0.000887793|0.001635577||
||**W.gcx**|12|0|||**W.htr**|0|0||
||**L.gcx**|0.7|0|||**L.htr**|0|0||
||**e.vh**|4.04|0|||**ev.h**|0|0||
||**e.vc**|4.04|0|||**ev.c**|0|0||
||**NTU**|3.632772671|0|||**NTU**|0|0||
|Gas Coolers (A is the|||precooler|b is the|S 1c/t is for the gas heater and|||||
|Intercooler)|||||RecupS  is for the recuperator|||||

## _**6.4 Performance for the 6c/3t IHC Brayton Cycle**_ 

The performance estimates for the simple 6c/3t single intercooler recuperated Brayton cycle is provided in this section.  These results were developed using the similarity scaling models for the turbomachinery and the heat exchanger model describe earlier.     Figure 6.4 shows a schematic loop diagram of the 6c/3t IHC Brayton cycle.  This complicated system of many heaters, coolers, turbines and compressors was selected based on earlier simple cycle analysis that indicated that efficiencies up to 56% could be achieved. However has mentions the materials limits of the reactor and primary heat exchanger limit the primary heat exchanger inlet temperature which requires a pressure ratio per set of 2 compressors to be about 3.4.  This “high” pressure ratio is reduces the ideal cycle efficiency to 51or 52%.  The proposed 6c/3t configuration presented here actually achieves efficiencies in the low 50 % range and the purpose of this analysis was to determine just what design features need to be adopted to obtain the high efficiency of 50%. 

As descried above, this figure shows the nomenclature used to identify locations at the various stations around the loop.  Station 1 always starts at the compressor inlet.  Station 2 is the compressor outlet, and these values increase around the loop.  The first compressor along the 

flow path is labeled with a subscript a or A, followed by b or B.  This proposed loop uses a pure helium primary loop and a separate gas in the Brayton cycle. 

![](images/tmpfjnpspht.pdf-0074-01.png)

**----- Start of picture text -----**<br>
Circulator<br>Trx_in Tsrc<br>Reactor<br>3 HTRA HTRB HTRC<br>4a 4b 4c<br>5<br>T A C F C E TB CD CC TC C B CA<br>1f 1e 1d 1c 1b 1a<br>GCXF GCXE GCXD GCXC GCXB GCXA<br>Tsnk<br>6 Water<br>3 5<br>3<br>Recuperator<br>6<br>2<br>**----- End of picture text -----**<br>

**Figure 6.4:  Multiple IHC Closed Brayton Cycle (CBC) having three turbine sets and six compressor sets.  (6c/3t CBC configuration).** 

## **6.4.1 Helium Argon Gas Mixture Configuration for the 6c/3t IHC Loop** 

The table of the cycle performance and the turbomachinery design for the 6c/3t Brayton loop is provided in Table 6-13.  The same nomenclature as described earlier is used here.  Note that for the 6c/3t system the net electrical efficiency is 50.4%, though the cycle analysis gives 53.0%.   This reduction in efficiency is due largely to the inefficiency of the generator and the circulator which had efficiencies of 98% and 97.1% respectively. 

The predicted efficiencies for the compressor and turbine are provide in 

Table 6-14.  This table shows that efficiencies vary through each compressor and each turbine. In general the high pressure compressor efficiency are lower than desired because the high pressure tends to lower the specific speed.  Note that we have selected a gas mixture so that the turbine efficiencies begin to approach the low 90% range which can be achieved for advanced turbine designs. 

**Table 6-13:  Results of cycle and turbomachinery analysis for the He/Ar IHC 2c/1t system with one intercooler.  Cycle efficiency is 45.8%, compressor efficiency was estimated to be 89.7% and the turbine efficiency was estimated to be 92.9%.** 

## **Table 6-14:  Turbomachinery Efficiency for the 6c/3t IHC He/Ar Brayton Cycle based on the similarity Analysis.** 

The thermal hydraulic performance and the mass estimates for the heat exchangers for the 6c/3t He/Ar Brayton cycle is listed in Table 6-15 and in Table 6-16.  The gas chiller information is shown in Table 6-15 and the heater information in Table 6-16. 

**Table 6-15;  Thermal hydraulic performance of the gas coolers in the 6c/3t IHC He/Ar gas Brayton cycle** 

**Table 6-16:  Themal hydraulic performance of the gas heaters and re-heaters in the 6c/3t IHC He/Ar (70/30) gas Brayton cycle.** 

## **7 Cost Performance and Trades** 

The IHC Brayton cycle involves additional components and places additional requirements on heat exchangers, turbomachinery and ducting.  The cost of the additional hardware as a function of the efficiency or effectiveness, and the estimate of the value of IHC modifications in terms of the additional electricity produced by the higher cycle efficiency, defines the cost benefit of this advanced cycle configuration.  In general, the efficiency of a power conversion cycle can be increased by increasing component efficiency or effectiveness, or the number of components that make up the cycle until the additional component cost is not recoverable from the additional electrical output from the power plant.  These cycle modifications must be considered in the context of the characteristics of the reactor heat source, such as inlet and outlet temperature and system pressure requirements.  The estimated cost of the optimized cycle is added to the cost of the heat source and other plant elements to arrive at a total cost for the power generating system. 

For the IH&C Brayton cycle the major components driving the PCS costs are turbines, compressors, generators, recuperation heat exchanger, rejection heat exchangers, input heat exchangers, cooling towers, electrical generator.  Relative estimates of these cost drivers will be sufficient to compare a standard recuperated Brayton cycle to the IHC Brayton cycle.  The 

following sections summarize the basic considerations used to define the cost framework to be used in this comparison.  Absolute cost estimates for the major components of a high temperature Brayton cycle at this stage of development are clearly uncertain, but the relative cost comparison of similar cycles (standard recuperated vs IHC) should provide a basis for evaluating the merit of these advanced cycles for next generation reactors. Since the goal is to provide a cost relevant figure of merit that can be used to identify the more promising research paths for Generation IV, an incremental cost benefit approach was developed based on changes from a reference recuperated helium Brayton cycle.  Costs for a similar system were developed in the GCRA study which provided a reasonable baseline for modified cycle cost comparisons. Although any such approach will involve degrees of approximation, the approach of using incremental costs compared to a better defined baseline should be applicable for a reasonable range of assumptions. 

## _**7.1 Relative cost Approach**_ 

For this initial analysis, a Figure of Merit (FOM) will be defined as the relative cost of electricity from the IH&C cycle as compared to the reference (baseline) recuperated Brayton cycle under the same conditions to pay off the capital investment. 

- FOM = ($/kWhr IH&C/ $/kWhr reference) 

The FOM directly relates to a reduced or increased cost of generated electricity.  (FOM of less than 1 = reduced generation costs). To relate this FOM to cycle efficiency and the PCS costs, the following simplified definitions will be used: 

- ($/kWhr = (RX + PCS) / (Pth*eff*D) 

where, RX = reactor capital cost recovery 

PCS = power conversion system capital cost recovery 

Pth = Source thermal power eff =  plant efficiency (ratio assumed equal to cycle efficiency) D = plant duty cycle 

The ratio of the cost of electricity from the IH&C cycle to that for the reference case is, 

- FOM  = [(RXIH + PCSIH) / (PthIH*effIH*DIH)] / [(RXR + PCSR) / (PthR*effR*DR)] 

If thermal power (Pth) and plant duty cycle (D) is similar for the two cases and thus cancel out in the definition of FOM 

- FOM =  [(RXIH + PCSIH) / (effIH)] / [(RXR + PCSR) / (effR)] 

If the RX (primarily independent of the PCS component costs) is also the same for the two cases, then this equation reduces to 

- FOM =  [(RXR + PCSIH)* effR ]/ [(RXR + PCSR)* effIH] 

For the reference system RXR is 78.28% and PCSR is 21.72%. 

- FOM =  [(78.28% + PCSIH) / (effIH)] / [(100%) / (effR)] 

- FOM =  (78.28% + PCSIH)* effR / effIH 

Where the sum of the RX and PCS can be referred to as the relative plant cost 

- FOM =  (Relative plant cost)* effR / effIH 

Only this relative plant cost and the ratio of the efficiency is required to evaluate the FOM. 

## _**7.2 Analysis Sequence**_ 

The sequence of calculations performed to develop the basis for this FOM was as follows: 

1. A first order assessment of the reference (direct recuperated He Brayton as costed in GCRA study), indirect recuperated using two stages of cooling and IH&C cycle configurations using 6 stages of cooling and 3 stages of heating is performed to define efficiency for the reference conditions.  These calculations are summarized earlier in this report. 

2. The major components required for these cycles are estimated and summarized according to key characteristics – size, weight, materials conditions etc – that control the costs for these components.  The major components are: 

   - a. Heat exchangers (recuperator, input, rejection) 

   - b. Turbines 

   - c. Compressors 

   - d. Generator 

   - e. Heat Rejection system (cooling tower, etc.) 

3. Based on simplified cost algorithms (described below), the relative cost of the major PCS components was calculated and compared to the reference cycle component costs. (Reference component costs were derived from the GCRA design study on high temperature gas reactors). 

4. A relative PCS system cost is determined by the ratio. 

5. This relative PCS is added to the fixed RX cost to obtain a “relative plant cost”. 

6. This “relative plant cost” is then multiplied by the ratio of the reference efficiencies of the reference system to the new system to arrive at a FOM for the cycle. 

The major factors determining component costs, size, number and complexity were identified, and the cost implications assigned based on algorithms for each component type.  Although only the major components were analyzed, the incremental analysis approach used here essentially scales all PCS costs (as compared to the reference) by the same ratio - increasing the PCS cost in proportion to the major components.   For this analysis, the cost of the MHGTR-Helium Direct Brayton was used as the reference component costs (as a percentage to account for difference in total thermal power). Cost comparison is accomplished by evaluating the modified system components to the reference system. 

For the heat exchanger size, the engineering analysis set the length of the heat exchanger to 0.7 meter and then adjusted the hydraulic diameter and flow area to arrive at a desired pressure drop.  With that hydraulic diameter and flow area, the size of the heat exchanger is determined. An alternative way of sizing the heat exchanger is to set the heat exchanger technology (for 

example 0.5mm size flow paths) then force the flow path length to be shorten to obtain the desired pressure drop.  This method sets the heat transfer coefficients to be fixed in all heat exchangers and sets a lower bound to the heat exchanger sizing.  Both methods are reported in this cost assessment. 

## _**7.3 Component Cost Relationships**_ 

## **7.3.1 Heat Exchanger Costs** 

This report assumes that the heat exchanger costs is proportional to the physical size of the heat exchangers and potentially service requirements and conditions.  Multipliers are employed to account for the service conditions (high temperature, pressures, etc., or lack of severe requirements) which relate the cost of the input HX and rejection HX to the recuperator HX. Multipliers used in this study range from 1.5 for the high temperature high pressure nuclear boundary components (input HX), to 0.375 for the much less demanding heat rejection components.  Although this approximation is intended to account for the varying degrees of sophistication in different applications, and thereby make the calculations more realistic, the multipliers obtained from competitive bids could be different than those used. 

A wide range of heat exchanger designs and materials can be considered, including plate, platefin, tube and shell, printed circuit (compact) and others.  For illustrative purposes diffusion bonded, micro channel heat exchangers, commonly referred to as printed circuit heat exchangers (PCHE) will be used.  PCHE’s provide a high surface area per unit volume heat exchanger, with flow passage sizes as required and the capability for high pressure differentials. In theory the pressure drop across these units can always be reduced by reducing the flow length and increasing the flow area, in practice there is a limit to this reduction due to the thermal conduction from the high-temperature and low-temperature sides of the heat exchanger.  As the effectiveness of the heat exchanger is increased, the total surface area for heat transfer will increase.  This increase in surface area will be reflected by an increase in the physical size, mass and cost of the heat exchanger. The heat exchanger volume or mass can be used to scale heat exchanger cost. 

Since previous studies have shown that the IH&C cycle is less sensitive to the input and rejection HX effectiveness, a simple optimization examination is conducted for the IH&C system to examine how the FOM is impacted by HX effectiveness variations. 

For the heat exchanger size, the effectiveness and  Tprimary/  Tsecondary (usually refered to as C ratio in heat exchangers) flow ratios are used to obtain a relative size.  This relative size is then use to obtain a relative cost based upon the temperature, and primary coolant primary boundary requirement for the heat exchanger.  When the heat exchanger is operated at the reactor outlet temperature and is a primary coolant barrier, it is assigned a multiplier of 1.5 to the baseline recuperator value.  When the heat exchanger is operated at the recuperator temperature and is a primary boundary, it is given a multiplier of one to the baseline recuperator value, since that is the function of the direct cycle recuperator.  When the heat exchanger is operated at the recuperator temperature and is not a primary boundary is is given a multiplier of 0.75.  When the heat exchanger is operated at the heat rejection temperature and is a primary coolant barrier it is given a multiplier of 0.50.  When the heat exchanger is operated at the rejection temperature and is not a primary barrier, it is given a multiplier of 0.375.  These multipliers are 

an attempt to include some of the cost associated with high temperature operation as well as Primary Reactor coolant containment cost.  Table 7-1 shows the relative size and cost for the heat exchangers for the direct cycle single stage compression, indirect cycle single stage heated and 2 stage cooled and the indirect cycle 6 stage cooled 3 stage heated cycles with set effectiveness for both He/Ar mixture and 100% Helium with fixed flow length.  Table 7-2 shows the relative size and cost for the heat exchangers for the same conditions with fixed hydraulic diameters. 

**Table 7-1:  Heat Exchanger Characteristics and Relative Costs based upon fixed flow lengths.** 

**Table 7-2:  Heat Exchanger Characteristics and Relative Costs based upon fixed hydraulic diameter.** 

## **7.3.2 Turbines/Compressor Costs** 

The turbine cost is driven by both size and complexity.  Complexity includes operating characteristics such as temperature, number of blade sets to achieve pressure ratio change, and flow area to achieve volumetric flow area required.  For very high temperature turbines, features such as ceramic or single crystal turbine blades and/or turbine blade cooling may be needed, but are probably not required for Gen IV applications. For this study, turbine cost is assumed to scale linearly with the turbine diameter, blade length, and the number of rotor/stator stages to achieve the desired pressure change. Larger turbine diameters are anticipated to impact rotor, stator and bearing designs, and all these cost are lumped into this size cost scaling relationship. 

For the recuperated Brayton cycle and the IH&C cycle, the mass flow rate is determined by the simple equation: 

Qin = mdot*cp*  T  and   Qin = mdot*cp*(  Ta+  Tb+  Tc) 

Where cp is the specific heat of helium,  T is the temperature rise of the helium going through the input heat exchanger (  Ta+  Tb+  Tc for the IH&C cycle) and mdot is the helium mass flow rate.  For both the recuperated and IHC cycles, the  T is always taken as 400°C to facilitate the  T desired in the reactor coolant flow. As a result, the mass flow rate for the “3t/6c” IHC cycle is approximately 1/3 that of the recuperated Brayton cycle, and the IHC turbine will have to operate at a lower pressure and/or have smaller blade lengths to achieve the proper flow angles in the turbines. 

The turbine inlet temperatures and pressure ratio across the turbine in this report are similar to those used in the MHGTR report (850°C to 950°C) and this report will use the turbine cost as 3.12% of the total cost for the “1t/2c” Brayton cycle.  Other Brayton cycle turbine cost will be scaled to this cost by the relative size. 

Compressor cost follows the same rules as the turbine cost.  As a result, the cost to achieve the pressure ratio is driven by the size of the compressor blades, and the number of stages.  The turbine/compressor design will be different for the 70%Helium/30%Argon system and the 100%Helium system.  Table 7-3 shows the engineering assessment for both systems. 

**Table 7-3:  Turbine and compressor size data for the three cycles considered.** 

## **7.3.3 Generator Costs** 

For electrical generators, magnetic field strength and coercive force are important factors in estimating the cost of the electrical generator.   The magnetic field strength times the frequency of operation results in the generator output voltage per unit size.  The coercive force sets a limit on the amount of current that can be drawn from the generator and is not frequency dependent. As a result, the power density of a generator varies inversely with frequency, however, for this study, the generating frequency will always be set at 60 Hz. The MHGTR study estimated the generator cost as 3.63%, of the total plant cost and as the cycle efficiency improves, that cost must increase proportionally with the output power.  At a total plant cost of $1500/kWe this gives a generator cost of ~$54/kWe.  Figure 7.1 shows the current cost of commercial small generators as a function of total output powers.  The unit cost trend appears to support a somewhat reduced generator cost than was used in the MHGTH study, however, these commercial small generators are expected to be substantially less efficient than what would be utilized in a large power plant as a result, for this study we will scale the cost using the generator cost of 3.63% used in the MHGTH study.  In addition, the generator cost must be adjusted for improved cycle efficiency, since additional power will be generated per thermal input power.  Therefore, the cost of the generator is proportional to the input power time the cycle efficiency and for this study will be adjusted by the ratio of the new cycle efficiency divided by the reference cycle efficiency. 

## **cost/kW vs total electrical power** 

![](images/tmpfjnpspht.pdf-0086-01.png)

**----- Start of picture text -----**<br>
$180<br>$160<br>$140<br>$120<br>$100<br>$80<br>$60<br>$40<br>$20<br>$0<br>1 10 100 1000 10000<br>Total electrical power (kW)<br>cost/kW electrical ($/kW)<br>**----- End of picture text -----**<br>

**Figure 7.1:  Per unit cost of small scale (<1MW) commercial generators as a function of power output** 

## **7.3.4 Heat Rejection Heat Exchangers** 

Heat rejection cost is proportional to the total thermal energy being rejected from the cycle. Higher efficiency results in lower heat rejection requirements. The cost of the heat rejection components depends upon the technology chosen.  The MHGTR report used a heat rejection cost of 2.26%.of total plant costs.   This represents a cost range between approximately $20/kWthermal based on $1500/kWe total plant cost.  Figure 7.2 shows the cost per thermal energy rejected for a range of heat rejection systems from a commercial cooling tower fabricator (Cooling Tower Systems, Inc.).  The cost for these cooling towers approach an approximate asymptotic value of  $15/kWthermal rejected which further supports the MHGTR heat rejection cost.  For this phase of the study, the cost of the heat rejection system will be taken as 2.26% adjusted for the total thermal energy being rejected in the assessed cycle compared to the baseline cycle (1-effIH&C)/(1-effR) 

## **cooling tower cost/kW vs total rejection power** 

![](images/tmpfjnpspht.pdf-0087-01.png)

**----- Start of picture text -----**<br>
$60<br>$50<br>$40<br>$30<br>$20<br>$10<br>$0<br>10 100 1,000 10,000<br>total rejection power (kW)<br>cost/kW<br>**----- End of picture text -----**<br>

**Figure 7.2:  Per unit cost of commercial cooling towers as a function of size.** 

## _**7.4 Description of Cycle Configuration**_ 

The system analysis undertaken to complete Task 1 (identified earlier in this report) assesses 

- the number of blade set and blade set sizes for both compressor and turbines, 

- the size of all heat exchangers, 

- the pressure drops through the system, 

- the thermodynamic efficiency of the cycle, and 

- the total pumping loss for any indirect driven cycles 

## _**7.5 Preliminary Cost Comparisons**_ 

Component cost estimates are based on the IH&C component sizes and characteristics. Based on plant efficiency calculations and the relative cost increments for IH&C components, the figure of merit can be given for the IH&C configuration.   The FOM is; 

FOM = ($/kWhr IH&C / $/kWhr reference) 

FOM = (Relative plant cost)* effR / effIH 

A FOM of 1 indicates that the incremental cost and efficiency improvements are offsetting.  A FOM of less than 1 indicates that the cost of electricity generation would be reduced by a fraction (1 – FOM), and a FOM of greater than 1 indicates that the cost of electricity generation would be increased by a fraction (FOM-1).   Table 7-4 gives the FOM for the 1173K source system with minimum reactor flow to decrease pumping power requirements based upon fixed HX flow length and Table 7-5 shows similar results with fixed HX hydraulic diameters 

**Table 7-4:  Relative component cost and FOM for HX with fixed flow length.** 

**Table 7-5:  Relative component cost and FOM for HX with fixed hydraulic diameter.** 

Although these are approximate results based on non-optimized configurations, it is apparent that for the conventional Brayton cycle configuration chosen as a reference, the additional constraints imposed by the reactor temperature difference limits and turbomachinery requirements significantly reduce the potential benefit for those configurations. 

## _**7.6 Cycle Optimization Considerations**_ 

In order to properly compare the relative costs associated with the standard recuperated and IHC cycles and their configurations, each system needs to be individually optimized first.  Two approaches are possible, the first would involve the trade-off of future revenues with the component cost, and the second involves the adjustment of the component cost to find the minimum in the FOM.  The first of these techniques involves the accurate knowledge of the component cost, associated cost and power plant revenue; while the second involves the 

iterative optimization for the minimum FOM as a function of components effectiveness. For this report, the actual cost of the equipment is not used but instead what is used is the relative cost between cycles and configurations.  This relative cost includes installation, preparation, and other associated costs.  As a result evaluating component cost increase may not take into account all of the multipliers that go with that cost.  For this study, we will iterate on the efficiencies of components where their effectiveness are impacted cost and find the relative minimum for the FOM.  The components that will be use adjusted will include the input, recuperator, and rejection heat exchangers, since the turbine and compressor effectiveness is assumed technology driven.  The fractional pressure drop through the system can be adjusted in various ways, and its impact and optimization will not be examined at this time. 

Figure 7.3 shows the FOM as a functional relationship of recuperator input effectiveness, where the original effectiveness was assumed at 95% and costing 7.11% of the total plant cost. This curve clearly shows the justification of the 95% effectiveness chosen for the recuperator, since it is at that recuperator effectiveness that the minimum FOM is obtained.  The recuperator and rejection effectiveness will also be evaluated to obtain the minimum FOM.  Similar analysis will be conducted on the remaining configurations to determine the minimum FOM. 

Figure 7.4 shows a similar plot of the FOM for the 3t/6c system as a function of the input heat exchanger effectiveness.  For this analysis, the heat exchanger hydraulic diameter was held constant, and the input heat exchanger effectiveness varied to determine the relative cost on heat exchangers and the resultant cycle efficiencies.  This plot indicates that FOM can still be optimized for the IH&C system; however, it is unlikely to fall below 1 with the given constraints. 

![](images/tmpfjnpspht.pdf-0089-03.png)

**----- Start of picture text -----**<br>
2.0<br>1.8<br>1.6<br>1.4<br>1.2<br>1.0<br>0.8<br>0.6<br>0.4<br>0.2<br>0.0<br>0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1<br>recuperator  effectiveness<br>FOM<br>**----- End of picture text -----**<br>

**Figure 7.3:  FOM for Direct Cycle Helium Recuperated Brayton as a function of the recuperator effectiveness.** 

![](images/tmpfjnpspht.pdf-0090-00.png)

**----- Start of picture text -----**<br>
FOM for 3t/6c as a function of input HX effectiveness<br>1.40<br>1.35<br>1.30<br>1.25<br>1.20<br>1.15<br>1.10<br>70% 75% 80% 85% 90% 95% 100%<br>input HX effectiveness<br>FOM<br>**----- End of picture text -----**<br>

**Figure 7.4:  FOM for 3t/6c He/Ar Brayton as a function of input HX effectiveness with HX flow path hydraulic diameter held constant.** 

## _**7.7 Figure of Merit Summary and Observations**_ 

The objective of this study was to evaluate the cost benefit of a more efficient IH&C Brayton cycle compared with the less complex standard recuperated cycle.  The approach taken was to compare a conventional Brayton configuration with and without interstage heating and cooling. The reference recuperated Brayton cycle was used establish a baseline cost and the incremental costs were then estimated and compared.   Although any such approach will involve degrees of approximation, the approach of using ratios of incremental costs compared to a well defined baseline should be applicable for a range of assumptions. 

Based on the preliminary configurations evaluated, the more detailed constraints placed on the cycle analysis by the reactor temperature constraints and the turbomachinery requirements significantly reduce the cost benefit of the IHC approach for the conventional configurations. This preliminary evaluation illustrates the complexity when turbomachinery design considerations (pressure drops, tip speeds, number of stages, blade lengths) are explicitly included in the cycle analysis.  In general it appears that when these additional constraints are included, the efficiency and therefore the cost advantages predicted by simple cycle analysis are reduced. 

This analysis suggests that other configurations (less common but still within current capabilities), such as dual shaft arrangements, where the first turbine drives multiple compressors (and perhaps a high frequency generator/motor for control) and the second turbine drives a 60 Hz generator, the IHC modifications would involve less cost penalties and still achieve the higher efficiency.  The next stage of these studies will address these options. 

## **8 Summary and Conclusions** 

The purpose of this study was to examine the turbomachinery and heat exchanger implications of interstage heating and cooling configurations.   In general, this analysis illustrates that these engineering considerations introduce new constraints to the design of IHC systems that may require different power conversion configurations to take advantage of the possible efficiency improvement.  Very high efficiency gains can be achieved with the IHC approach, but this can require large low pressure turbomachinery or heat exchanger components, whose cost may mitigate the efficiency gain.  One stage of interstage cooling is almost always cost effective, but careful optimization of system characteristics is needed for more complex configurations. The following list summarizes the primary factors that must be considered in evaluating the IHC configurations that may lead to more efficient cycles. 

- The 3t/6c IH&C Brayton cycle system appears to be no larger than current Rankine cycle systems.  Sizes are similar because they have similar pressure in the low pressures leg of the loop. 

- Even when constrained by VHTR inlet and outlet temperatures, plant thermal efficiencies can be improved from the low to mid 40% range to the low 50% range with multiple interstage heating and cooling implementation.  Designs for the IHC configurations can be developed that do indeed achieve the high efficiencies that are were reported earlier. 

- Multiple techniques can be used to match the specific speed and specific diameter requirement of the turbo/compressor systems.  Changing the molecular weight is one approach that allows the turbine and compressor to operate at specific speeds that allow highly efficient turbomachinery.  Another approach is to spin the turbomachinery faster, but this entails frequency conversion of some type. 

- Primary coolant recirculators appear to be both technically reasonable and not an undue penalty to the system efficiency.  The inefficiencies of the primary gas circulator increases the enthalpy of the primary loop which allows the power conversion system to extract about 40-50% of this energy out as electrical power.  Effective circulator efficiency appears to be as high as 97% based on our similarity analysis modeling approach. 

- Significant variations in the Figure of Merit (FOM) can be obtained depending upon the design assumptions for the system heat exchangers (two assumptions were used in this report).  Due to the complexity of the 6c/3t IHC Brayton system a large number of parameters may be varied to optimize for system costs.  The systems evaluated in this report are clearly not optimized, but are intended to represent a reasonable operating configuration. 

- The 3t/6c IHC system as proposed here appears to be a marginal cost benefit. Other configurations are suggested by these analyses may offer better cost benefits. These could include systems with two turbines and four or more compressors.  Alternatively, the system pressure could be increased.  Likewise a power turbine configuration could be applied that allows the electrical power turbine to spin at 3600 rpm while a second shaft and set of turbines spins at much higher frequency to run the main compressor. 

- A major advantage of the 6c/3t IHC system is that it is very insensitive to pressure drop.  It is also insensitive to the effectiveness of the gas heater/re-heater and precooler/intercooler heat exchanger effectiveness. 

- Other constraints may force the use of IHC systems, including (1) controllability of system, (2) excessive pressure drop in system, and (3) insensitivity to component effectiveness. 

Future work to determine cost effective approaches to more efficiency gas Brayton cycles is warranted.  Based on the analysis performed in this study it was shown that the use of a single stage of intercooling almost always was worth pursuing because of the gain in efficiency comes at very little cost in complexity.  However the analysis also showed that substantial efficiency gains could be achieved with more complex Brayton cycle configurations but at added costs.  For the multistage IHC system with six compressors and three turbines it appears that advantages gained are offset by the additional costs, but there are a number of intermediate IHC systems that should be considered.  Two such systems are obvious candidates.  In the first system two stages of intercooling can be used instead of one stage.  The second improvement on the IHC system is to use a system with two turbines and fours levels of intercooling.  The approach or goal here is to find the optimum configuration that balances additional costs with improvement in efficiency. 

Another system that needs further examination is one that uses two shafts and one stage of re-heat.  In this configuration one shaft spins the main turbine and power generator at 3600 rpm.  The gas molecular weight and number of stages can be used to obtain the correct specific speed and high turbine efficiency for this shaft.  The second shaft spins a compressor and a small non-synchronous generator to control the shaft speed.  This shaft spins over a range of speeds that can be used for load following and for control.  Because it spins faster than 3600 rpm it can be made smaller and at reduced costs.  This design introduces a level of flexibility and control not available to the single shaft system. 

Finally, another alternative power conversion configuration uses bottoming cycles.. Designs that use steam as the bottoming cycle are all readying being proposed by the French fast gas reactor concept.  However, it is warranted to examine supercritical CO2 or other supercritical fluids (generally high molecular weight refrigerants) as the bottoming cycle.  We have only briefly looked at these systems and can see that thermal matching and the magnitude of recuperation are important issues that impact the cycle efficiency for these bottoming cycles. 

## **References** 

Balje O. E., Turbomachines:  A Guide to Design, Selection and Theory, John Wiley and Sons, New York, 1981. 

Baxi C.B., et. al., “Evolution of the Power Conversion Unit Design of the GT-MHR”, in proceedings of the 2006 International Congress on Advances in Nuclear Power Plants (ICAPP 06), Reno June 4-8, 2006. 

Brey, H. L. “Current Status and Future Development of Modular High Temperature Gas Cooled Reactor Technology,” IAEA, Tecdoc=(electronic version ), 1999-2000. 

Buckingham E. “On physically similar systems: illustrations of the use of dimensional equations”, Physical Review 4(4): 345, 1914. 

Chapman, Alan J. Heat Transfer, Macmillan Company, NY, 1967. 

Electronics Online, http://www.electroline.com.au/elc/feature_article/item_112001a.asp, 2001. 

GCRA, “Modular High Temperature Reactor Commercialization and Generation Cost Estimates”, HTGR-90365, August, (1993). 

Holman, J. P.,Heat Transfer, McGraw-Hill, New York, NY, 2001. 

Japikse, D. and N.C.  Baines.  Introduction to Turbomachinery, Concepts ETI Inc. and Oxford University Press, 1997. 

Japikse, D. Centrifugal Compressor Design and Performance, Concepts ETI Inc. 1996. 

LaBar, M. P., 2002. The gas turbine–modular helium reactor:  a promising option for near term deployment. _Proc., International Congress on Advanced Nuclear Power Plants, Embedded Topical American Nuclear Society 2002 Annual Meeting, Hollywood, Florida, June 9–13, 2002, GA-A23952._ 

Mathsoft Engineering and Education, Inc., 101 Main Street, Cambridge, MA 02142-1521, www.mathcad.com, 2006. 

Mitchell C, Poette C., et. al., “GCFR: The European Uniso’s Gas Cooled Fast Reactor Project”, in Proceedings of the 2006 International Congress on Advances in Nuclear Power Plants (ICAPP 06), Reno June 4-8, 2006. 

NASA, Software Repository, https://technology.grc.nasa.gov/software/index.asp, 2005. 

Peterson, P. F., 2003a. Multiple-reheat Brayton cycles for nuclear power conversion with molten coolants. _Nucl. Technol.,_ **144** , 279–288. 

Peterson, P.F., et. al., 2004. Next generation nuclear plant power conversion study: technology options assessment, _Generation IV Program._ 

Pope M. A. Driscoll M. and Hejzlar P. “Reactor Physics Studies in Support of GFR Core Design”, Transactions of the American Nuclear Society, Proceeding of  GLOBAL ’03, New Orleans, LA, Nov. 16-21, 2003. 

Saito, S., et. al, “Design of High Temperature engineering Test Reactor (HTTR), JAREI 1332, 6 1994. 

Shepard D. G, “Principles of Turbomachinery, Macmillan, New Yourk, 1957. 

Walsh P.P. and P. Fletcher. Gas Turbine Performance, ASME Press, 1998. 

Wasserbauer, C.A. and A.J.Glassman.  “FORTRAN Program for Predicting Off-Design Performance of RadialInflow Turbines,” NASA TN D-8063, 1975. 

Wilson D. G., The Design of High-Efficiency Turbomachinery and Gas Turbines, MIT Press, Cambridge, Massachusetts, 1988. 

