---
source: "https://engineering.purdue.edu/CMUXE/Publications/AHR/R88ORNL-FEDC-87-7.pdf"
source_type: "url"
extracted_at: "2026-09-19T01:18:20.144403+00:00"
content_hash_sha256: "23e24fb7e722fbb74eb6cff7212881c199f6d9707c9c7b3f5c89ec5398ba3754"
backend: "pdf_pipeline"
---



![](images/tmp2afbqpn1.pdf-0002-18.png)

|**`Figure`**|||
|---|---|---|
|**`1.1`**|**`Constrained optimization of a figure of merit leads to`**||
||**`acceptable and unique design points`**|**`1`**|
|**`2.1`**|**`Tokamak reactor systems flow diagram.........`**|**`7`**|
|**`2.2`**|**`Experimental test reactor tokamak systems code schematic...`**|**`8`**|
|**`1.1`**|**`Reference TIBER II poloidal field divertor magnetics`**||
||**`configuration (K69B) illustrating closed internal flux`**||
||**`surfaces (solid lines) and open external flux surfaces`**||
||**`(dashed lines) leading to an Idealized divertor "plate"`**||
||**`at R - 2.0 m and z - ±2.75 m (dotted lines)`**|**`32`**|
|**`1.2`**|**`Expanded view of TIBER II poloidal field divertor magnetics`**||
||**`configuration (K69B)`**|**`33`**|
|**`1.3`**|**`Schematic of torus vacuum puaping system`**|**`39`**|
|**`1.1`**|**`Essential and nonessential facility power system one-line`**||
||**`diagram`**|**`57`**|
|**`1.5`**|**`Coil power supply system one-line diagram (direct utility`**||
||**`line connection option)..`**|**`58`**|
|**`1.6`**|**`Coil power supply system one-line diagram (motor-generator/`**||
||**`flywheel option)`**|**`59`**|
|**`1.7`**|**`Power conversion and protection system for the toroidal`**||
||**`field magnets..`**|**`76`**|
|**`1.8`**|**`Typical three-channel signal conditioning for the toroidal`**||
||**`field coil protection system`**|**`77`**|
|**`1.9`**|**`Power conversion system for resistive toroidal field coils..`**|**`78`**|
|**`1.10`**|**`Code flow diagram for the toroidal field magnet power`**||
||**`conversion module TPCPWR`**|**`81`**|
|**`1.11`**|**`One-line diagram of a superconducting poloidal field coll`**||
||**`power conversion and protection system`**|**`89`**|
|**`1.12`**|**`A typical two-quadrant pulsed power supply module`**||
||**`integrated with a low-voltage burn supply power unit........`**|**`90`**|
|**`1.13`**|**`A typical four-quadrant pulsed power supply module`**||
||**`integrated with a low-voltage burn supply power unit`**|**`91`**|
|**`1.11`**|**`One-line diagram of a poloidal field power conversion`**||
||**`circuit with corresponding symmetrical colls connected`**||
||**`in series`**|**`93`**|
|**`1.15`**|**`One-line diagram of a poloidal field power conversion`**||
||**`circuit with corresponding symmetrical coils connected`**||
||**`in parallel`**|**`91`**|

|**`1.16`**|**`Computer software flow diagram for the PFPOW module`**|**`99`**|
|---|---|---|
|**`1.17`**|**`One-line diagram of the energy storage system with the`**||
||**`ISCENR switching logic`**|**`107`**|
|**`1.18`**|**`Block diagram of the energy storage module and its`**||
||**`interfaces with other code modules`**|**`108`**|
|**`1.19`**|**`Code flow diagram for the energy .-storage system module`**||
||**`ESTORE`**|**`Ill`**|

![](images/tmp2afbqpn1.pdf-0014-01.png)

![](images/tmp2afbqpn1.pdf-0018-00.png)

||**`TaM* 3.1. Description of nans! eat a IOC`**|||
|---|---|---|---|
|||**`Corresponding ICC`**||
|**`Constraint`**|**`Description of the constraint`**||**`variables`**|
|**`1`**|**`rololdal beta equation`**|**`2`**||
|**`2`**|**`Hot ion bean density equation`**|**`10`**||
|**`3`**|**`Beta calculation`**|**`It`**||
|*****|**Clonal power balance equation (tl/te - fixed)**|**4,**|**12, 15**|
|**5**|**Ion power balance**|**4, 11, 15**||
|**6**|**Electron power balance**|**4,**|**12, 15**|
|**T**|**"Density Unit equation**|**15,**|**17**|
|**c 8**|**"Beta ltnit equation**|**12.**|**15, 16**|
|**9**|**Radial build**|**9,**|**18, 19, 30. 8, 31**|
|**10**|**•Volt-second equation**|**25,**|**20, 29, 18, 19**|
|**11**|**•Bucking cylinder budding stress**|**32,**|**31**|
|**12**|**•Bucking cylinder bearing stress**|**23.**|**31**|
|**13**|**•neutron wall load equation**|**2*.**|**12, 15**|
|**1***|**•Inner shield equation (old first wall nodal)**|**28,**|**22.**|
|**15**|**•Outer shield equation (old first wall nodel)**|**35,**|**13**|
|**16**|**"Ohalc heating (OH) coil stress**|**27,**|**20, 45**|
|**17**|**"Toroidal field (TF) coil stress**|**36,**|**21, 30, 6, 3**|
|**18**|**Field at TF coll (- required field at TF coil)**|**1, 9, 21. 30**||
|**19**|**•Insulator dose**|**42,**|**22**|
|**20**|**•Shut-down dose rate**|**43. 13**||
|**21**|***TF coil port aize equation**|**5, 40**||
|**22**|***0H coil superconductor current**|**33,**|**20, 47, 46,45**|
|**23**|***TF coil superconductor current**|**26,**|**21, 41, 7, 3**|
|**24**|**"Sheffield figure of earit**|**39,**|**8, 9, 1**|
|**25**|**"Peak TF coil nuclear heating**|**44,**|**22**|
|**26**|**"Maxim* TF ooll field**|**37,**|**1, 9, 21**|
|**27**|**"Big Q value (injected power/fusion power)**|**34,**|**12, 15, 1, 9**|
|**28**|**"TF conductor stability ear gin**|**48, 41, 7, 3**||
|**29**|**"OH coll conductor stability Margin**|**49, 47, 46, 45**||

|**`Variable`**|**`Variable`**||||
|---|---|---|---|---|
||**`so.`**||`Syabol`|`Description`|
||**`i`**||`bt`|`Toroidal field (TF) on axis (T)`|
||**2**||**betap**|**Pololdal beta**|
||**3**||**thwcndut**|**TF coil conduit case thickness**|
||*****||**dign**|**Plasm ignition aargin**|
||**5**|**•**|**rtrport**|**f-value for Eq. (21)**|
||**6**||**thkcas**|**TF c o l l external case average thickness (a)**|
||**7**||**vftf**|**He fraction on inside of TF coll Minding pack**|
||**8**||**aspect**|**Plaaaa aspect r a t i o**|
||**9**||**major**|**Plasm aajor radius**|
||**10**||**rnbaaa**|**Hot bean ion density/electron density**|
||**11**||**tratio**|**Ion teaperature/electron taaperature**|
||**12**||**te**|**average electron teaperature (vol. averaged) (keV)**|
||**13**||**dsho**|**Outer shield thickness (a)**|
||**11**||**beta**|**Plasm beta**|
||**15**||**dene**|**average electron density (a~*)**|
||**16**|**•**|**rbeta**|**f-value for beta H a l t , Eq. (8)**|
||**IT**|*****|**fdene**|**f-value for density H a l t , Eq. (?)**|
||**18**||**soltx**|**Thickness of ohalc heating (OR) cafl (including case) (a)**|
||**19**||**boresol**|**Radius or OH coll inner bore (a)**|
||**20**||**coheof**|**Overall current density in OH coil at end of f l a t t o p (A)**|
||**21**||**rjeoatf**|**Conductor current density in TF coil (a)**|
||**22**||**dshi**|**Inner shield thickness (a)**|
||**23**|**•**|**fbcbr**|**f-value for bucking cylinder stress, Eq. (12)**|
||**2***|**•**|**rwalld**|**f-value for neutron wall load, Eq. (13)**|
||**25**|*****|**fvs**|**f-value for volt-second, Eq. (10)**|
||**26**|*****|**rcpttf**|**f-value for TF coll current, Eq. (23)**|
||**27**|**•**|**fohsts**|**f-value for OH coil stress, Eq. (16)**|
||**28**|**•**|**fdshl**|**f-value for inner shield thickness, Eq. (1«)**|
||**29**||**<x>hbop**|**Overall current density in OH coll at beginning o f pulse (A)**|
||**30**||**tfthkl**|**TF coil thickness (Including case) (a)**|
||**31**||**bcylth**|**Bucking cylinder thickness (a)**|
||**32**|*****|**fbckl**|**f-value for bucking cylinder, Eq. (11)**|
||**33**|*****|**fcptoh**|**f-value for OK coll currant, Eq. (22)**|
||**3***|**•**|**fqval**|**f-value f o r Q, Eq. (27)**|
||**35**|**"**|**fdsho**|**f-value for outer shield thickness, Eq. (15)**|
||**36**|**"**|**ftfsts**|**f-value for TF coll stress, Eq. (17)**|
||**37**|**•**|**fbaax**|**f-value for aaxiaun TF coil f i e l d , Eq. (26)**|
||**38**||**fefac**|**H-factor in Kaye-Goldaton conflneaent scaling**|
||**39**|*****|**ffigar**|**f-factor in figure of aerlt, Eq. (24)**|
||**40**||**dago**|**Cap between outboard TF coil leg and shield (a)**|
||**•1**||**fcutf**|**Copper fraction of TF ooll winding pack conductor**|
||**42**|*****|**ffwlrad**|**f-value for radiation dose H a l t , Eq. (19)**|
||**•3**|*****|**ffwladd**|**f-value for ahut-down dose H a l t , Eq. (20)**|
||**44**|**•**|**ffwlht**|**f-value****_tor_ TF coil nuclear heating, Eq. (25)**|
||**45**||**twedtoh**|**OH oo11 oondult case thickness (a)**|
||**46**||**vfohc**|**He fraction on inside of OH ooll winding pack**|
|**l,**|**47**||**fcuoh**|**Copper fraction of OK coll winding pack conductor**|
||**48**|*****|**faptf**|**f-value for TF coil conductor stability, Eq. (28)**|
||**49**|**"**|**fepoh**|**f-value for OH coll conductor stability, Eq. (29)**|

|**MINMAX**|Figure of merit|Description|
|---|---|---|
|0|dign|Plasma ignition' margin|
|1|rmajor|Plasma major radius|
|2|totdcst|Total direct cost|
|3|wallmw|Neutron wall load|
|`1`|`te`|`Plasma electron temperature`|

![](images/tmp2afbqpn1.pdf-0034-04.png)

![](images/tmp2afbqpn1.pdf-0035-04.png)

![](images/tmp2afbqpn1.pdf-0035-06.png)

![](images/tmp2afbqpn1.pdf-0035-07.png)

![](images/tmp2afbqpn1.pdf-0037-06.png)

![](images/tmp2afbqpn1.pdf-0037-10.png)

![](images/tmp2afbqpn1.pdf-0042-01.png)

![](images/tmp2afbqpn1.pdf-0043-01.png)

|**`Module`**|**`Lead Author`**|**`Organization`**|
|---|---|---|
|**`Torus configuration`**|**`J. D. Galambos`**|**`FEDC/ORNL`**|
|**`Torus vacuum system`**|**`J. R. Haines`**|**`FEDC/McDonnell`**|
|||**`Douglas`**|
|**`Fueling systems`**|**`S. K. Ho`**|**`LLNL`**|
|**`Torus support structure`**|**`L. J. Perkins`**|**`LLNL`**|
|**`Bucking cylinder`**|**`J. D. Galambos`**|**`FEDC/ORNL`**|

![](images/tmp2afbqpn1.pdf-0049-01.png)

![](images/tmp2afbqpn1.pdf-0049-02.png)

|**`Variable`**|**`Source`**|**`Description`**|
|---|---|---|
|**`ai`**|**`Physics`**|**`Plasma current (maximum design value) (A)`**|
|**`rO`**|**`Physics`**|**`Major radius (m)`**|
|**`a`**|**`Physics`**|**`Minor radius (n)`**|
|**`akappa`**|**`Physics`**|**`Elongation`**|
|**`bO`**|**`Physics`**|**`Axial B-field (T)`**|
|**`shldnass`**|**`Shield`**|**`Total mass of shield (kg)`**|
|**`dvtmass`**|**`Impurity`**|**`Total mass of divertor and associated`**|
||**`control`**|**`structure (kg)`**|
|**`pfmass`**|**`PF magnets`**|**`Total mass of PF coils plus cases (kg)`**|
|**`tfmass`**|**`TF magnets`**|**`Total mass of TF coils plus cases (kg)`**|
|**`tranht`**|**`Magnets`**|**`Height of central PF stack (ai)`**|
|**`tranbore`**|**`Magnets`**|**`Inner bore radius of central PF stack (m)`**|
|**`strucost`**|**`User input`**|**`Structure unit cost—materials and`**|
|||**`fabrication ($/kg)`**|
|||**`(if stHicost - 0, default - 28 $/kg`**|
|||**`is used)`**|
|**`nout`**|**`Main`**|**`Logical unit number for output print file`**|
|**`iprint`**|**`Main`**|**`Instruction to print results: 0/1 - no/yes`**|

|Module|Lead Author|Organization|
|---|---|---|
|ECH system|C. E. Wagner|TRW, Inc./LLNL|
|LH system|||
|NBI system|L. J. Perkins|LLNL|
|Alternating current (ac)|D. R. Hicks|FEDC/ORNL|
|power system|||
|Instrumentation and|D. R. Hicks|FEDC/ORNL|
|controls (I&C)|||

|**`Variable`**|**`Description`**|
|---|---|
|**`nlines`**|**`Total nuaber of beamlines`**|
|**`effcy`**|**`Total beamline efficiency—`**|
||**`injected power/wall-plug power`**|
|**`pvpop`**|**`Total wall-plug power required (W)`**|
|**`cost`**|**`Total cost of beamlines and power supplies ($)`**|
|**`qtorus`**|**`Room-temperature gas flow from beamlines into torus`**|
||**`vacuum (D 2/s)`**|
|**`zsrcplsm`**|**`Source—plasma distance (m)`**|
|**`zfocus`**|**`Distance: source to minimua focus between outer`**|
||**`TF coils legs (m)`**|
|**`zext`**|**`Length of beamline external to vacuum vessel (m)`**|
|**`wduct`**|**`Width of duct at minimum focus between outer TF coils`**|
||**`On) {«)`**|
|**`hduct`**|**`Height of duct (vertical direction) at minimum focus`**|
||**`(m) {«}`**|
||**`(*—if iduct - 0 in the input, this module calculates`**|
||**`wduct, hduct, and zduct; if iduct * 1, these`**|
||**`three variables are supplied externally and the`**|
||**`module computes beam parameters consistent with`**|
||**`these fixed dimensions)`**|
|**`wtf`**|**`Minimum permissible separation of outer TF coil`**|
||**`legs—case to case (m)`**|
|**`zduct`**|**`Distance from minimum focus point between outer`**|
||**`TF legs to tangential intercept at plasma axis`**|
||**`On) {«}`**|

|**`Variable`**|**`Variable`**|||||**`Description`**|
|---|---|---|---|---|---|---|
|**`pinj`**|**`- 43.90 HW`**|||||**`Total injected power requirement`**|
|**`ebeam`**|**`• 500.0 keV`**|||||**`Beam energy requirement`**|
|**`aibeam`**|**`- 87.80 A`**|||||**`Total injected current requirement`**|
|**`nllnes`**|**`- 2`**|||||**`No. of beamlines`**|
|**`effey`**|**`• 0.3372`**|||||**`Overall efficiency—injected`**|
|||||||**`power/wall-plug power`**|
|**`P«P`**|**`- 130.2 MW`**|||||**`Total wall-plug power`**|
|**`ucost`**|**`- 1.698 $/V`**|||||**`Neutral beam unit cost—$/W of wall-plug`**|
|||||||**`power`**|
|**`cost`**|**`- 2.210 «`**|**`1 0`**||**`8  `**|**`$`**|**`Total cost of beamlines and power`**|
|||||||**`supplies`**|
|**`nsource`**|**`- 2`**|||||**`No. of source arrays/beamline`**|
|**`ajsource`**|**`- 60.00 A/«`**||**`2`**|||**`Average source current density`**|
|**`a`**|**`- 0.1184 m`**|||||**`Source array width`**|
|**`b`**|**`- 9.472 m`**|||||**`Source array height`**|
|**`asource`**|**`- 4.486 m`**|**`2`**||||**`Total area of all sources`**|
|**`psource`**|**`- 0.0100 torr`**|||||**`Source pressure`**|
|**`paccl`**|**`- 1.0 * lO"*`**|||**`torr`**||**`Accelerator pressure`**|
|**`pneut`**|**`- 1.455 «`**|**`10"`**|||**`4 torr`**|**`Neutralizer inlet pressure`**|
|**`pnout`**|**`- 1.455 »`**|**`10"`**|||**`5 torr`**|**`Neutral`****_iter_****`outlet pressure`**|
|**`plaat`**|**`- 1.455 »`**|**`10"`**|||**`5 torr`**|**`Final line pressure`**|
|**`ptorus`**|**`- 1.0 * 10"`**||**`6  `**|**`torr`**||**`Torus vacuum pressure`**|
|**`qtorus`**|**`- 9.874 «`**|**`1`**|**`0`**|**`1 `**|**`9 mol/`**|**`Room temperature gas load to torus from`**|
|||||||**`all beamlines`**|
|**`ep`**|**`- 0.9500`**|||||**`Power supply efficiency`**|
|**`ea`**|**`- 0.8499`**|||||**`Accelerator (current) efficiency (power`**|
|||||||**`efficiency - accelerator efficiency/2`**|
|||||||**`• 0.5)`**|
|**`en`**|**`- 0.5800`**|||||**`Neutrallzer efficiency`**|
|**`el`**|**`- 0.9845`**|||||**`Final line efficiency`**|
|**`es`**|**`• 0.6721`**|||||**`Collimator skimmer efficiency`**|
|**`effcyl`**|**`- 0.3262`**|||||**`Beamline current efficiency`**|
|**`plossp`**|**`• 6.509 MW`**|||||**`Total loss in power supplies`**|

||**1Variable**|**`Description`**|
|---|---|---|
|**plossa**|**- 4.6*1 MW**|**`Accelerator loss per beamline`**|
|**plossn**|**- 24.02 MW**|**`Neutralizer loss per beamline`**|
|**plossl**|**- 0.5M7 Mf**|**`Final line loss per beamline`**|
|**plosss**|**- 10.71 MM**|**`Collimation skimmer loss per beamline`**|
|**zsrcaccl**|**- 3.200****_m_**|**`Source/accelerator length`**|
|**zneut**|**- 30.00 •**|**`Neutralizer length`**|
|**zlast**|**- 5.000 •**|**`Final line length`**|
|**zsrcplsm- 45.71 •**||**`Total line length from source to plasma`**|
|**zfocus**|**- 41.10 •**|**`Distance from source to minimum focus`**|
|**zext**|**- 38.20 •**|**`Length of beamline external to vacuum`**|
|||**`vessel`**|
|**efolda**|**- 0.690**|**`Collimator width in narrow direction`**|
|||**`(beam e-folds)`**|
|**wduct**|**- 0.412 •**|**`Width of duct at minimum focus between`**|
|||**`outer TF coil legs`**|
|**hduct**|**- 0.842 m**|**`Height of duct at minimum focus`**|
|**wtf**|**- 1.264 •**|**`Minimum permissible separation of outer`**|
|||**`TF coil legs`**|
|**zduct**|**- 4.610 n**|**`Distance from minimum focus to tangential`**|
|||**`intercept at plasma axis`**|

![](images/tmp2afbqpn1.pdf-0067-01.png)

![](images/tmp2afbqpn1.pdf-0068-01.png)

![](images/tmp2afbqpn1.pdf-0069-01.png)

![](images/tmp2afbqpn1.pdf-0079-02.png)

![](images/tmp2afbqpn1.pdf-0079-04.png)

![](images/tmp2afbqpn1.pdf-0079-06.png)

![](images/tmp2afbqpn1.pdf-0080-02.png)

![](images/tmp2afbqpn1.pdf-0080-05.png)

![](images/tmp2afbqpn1.pdf-0080-08.png)

![](images/tmp2afbqpn1.pdf-0081-02.png)

![](images/tmp2afbqpn1.pdf-0081-03.png)

![](images/tmp2afbqpn1.pdf-0081-06.png)

![](images/tmp2afbqpn1.pdf-0082-02.png)

![](images/tmp2afbqpn1.pdf-0082-04.png)

![](images/tmp2afbqpn1.pdf-0082-06.png)

![](images/tmp2afbqpn1.pdf-0082-08.png)

![](images/tmp2afbqpn1.pdf-0086-01.png)

![](images/tmp2afbqpn1.pdf-0087-01.png)

![](images/tmp2afbqpn1.pdf-0088-01.png)

![](images/tmp2afbqpn1.pdf-0094-01.png)

![](images/tmp2afbqpn1.pdf-0094-02.png)

![](images/tmp2afbqpn1.pdf-0099-02.png)

![](images/tmp2afbqpn1.pdf-0100-01.png)

![](images/tmp2afbqpn1.pdf-0101-01.png)

![](images/tmp2afbqpn1.pdf-0103-01.png)

![](images/tmp2afbqpn1.pdf-0104-01.png)

![](images/tmp2afbqpn1.pdf-0109-01.png)

![](images/tmp2afbqpn1.pdf-0110-01.png)

![](images/tmp2afbqpn1.pdf-0110-02.png)

![](images/tmp2afbqpn1.pdf-0111-01.png)

||||**Resistive**||||
|---|---|---|---|---|---|---|
||**Time**||**power**||**Total**||
|||**( 3 )**|**(MW)**||**MVA**||
|||**0**|**0**||**0**||
|||**0**|**0**||**0**||
|||**30**|**1.388**||**29.07**||
|||**30**|**1.388**||**-30.23**||
|||**50**|**1.738**||**121.1**||
|||**50**|**1.738**||**26.50**||
|||**56**|**1.933**||**28.48**||
|||**56**|**1.933**||**3.526**||
||**156**||**2.148**||**3.847**||
||**156**||**2.148**||**-249.2**||
||**168**||**0**||**0**||
||**168**||**0**||**0**||
|**PF coil**|**Maximum**||**Minimum**|**Maximum**|**Minimum**||
|**circuit**|**voltage,**||**voltage,**|**current,**|**current,**|**MVA,**|
|**No.,**|**VPFMAX**||**VPFMIN**|**CPTMAX**|**CPTMIN**|**PSMVA**|
|**PFCKT**|**(kV)**||**(kV)**|**(kA)**|**(kA)**||
|**1**|**0.1754**||**-0.2785**|**25**|**0**|**11.35**|
|**2**|**0.1751**||**-0.2785**|**25**|**0**|**11.35**|
|**3**|**0.2718**||**-0.8478**|**25**|**0**|**27.99**|
|**4**|**0.2718**||**-0.8478**|**25**|**0**|**27.99**|
|**5**|**0.0071954**||**-0.0060180**|**10.35**|**-25**|**0.4672**|
|**6**|**0.0071954**||**-0.0060180**|**10.35**|**-25**|**0.4672**|
|**7**|**0.8015**||**-0.5091**|**5.467**|**-25**|**39.93**|
|**8**|**0.8015**||**-0.5091**|**5.467**|**-25**|**39.93**|
|**9**|**2.141**||**-1.241**|**0**|**-25**|**84.53**|
|**10**|**2.141**||**-1.241**|**0**|**-25**|**84.53**|
|**11**|**0.2390**||**-0.2745**|**23.29**|**-25**|**24.79**|
|**12**|**0.2390**||**-0.2745**|**23.29**|**-25**|**24.79**|
|**13**|**1.696**||**-1.489**|**9.545**|**-22.57**|**102.3**|

![](images/tmp2afbqpn1.pdf-0117-01.png)

![](images/tmp2afbqpn1.pdf-0118-01.png)

|**`Code`**|**`Input`**|**`Expected`**|**`Mnemonic`**|
|---|---|---|---|
|**`mnemonic`**|**`module`**|**`range`**|**`description`**|
|**`PEAKMVA`**|**`PFPOW`**|**`100 to`**|**`Maximum peak NVA of all PF power`**|
|||**`1000 HVA`**|**`supplies combined`**|
|**`EMSXPFM`**|**`PFPOW`**|**`1000 to`**|**`Maximum stored energy in all PF coil`**|
|`•`||**`5000 MJ`**|**`circuits combined`**|
|**`ENGTPFM`**|**`PFPOW`**|**`4000 to`**|**`Maximum dissipated energy per cycle`**|
|||**`20000 NJ`**|**`for all PF coil circuits combined`**|
|**`TFIMAL -`**|**`PFPOW`**|**`200 to`**|**`Pulsed fusion power cycle time`**|
|**`TIM(8)`**||**`2000 s`**||
|**`EHSRPF(5)`**|**`PFPOW`**|**`500 to`**|**`Total energy to all PF coil circuits`**|
|||**`2500 MJ`**|**`at the beginning of the burn phase`**|
|**`ENSRPF(6)`**|**`PFPOW`**|**`4000 to`**|**`Total energy to all PF coil circuits`**|
|||**`20000 NJ`**|**`at the end of the burn phase`**|
|**`TBURN`**|**`PFPOW`**|**`200 to`**|**`Burn phase time interval`**|
|||**`2000 s`**||
|**`PFCKTS`**|**`PFPOW`**|**`5 to 20`**|**`No. of PF coil power supply circuits`**|
||||**`(NCIRT - 1)`**|
|**`FHEATMW`**|**`CUDRIV`**|**`50 to`**|**`Average plasma current drive/`**|
|||**`200 MW`**|**`heating power`**|
|**`PHTGMJ`**|**`CUDRIV`**|**`4000 to`**|**`Plasma current drive/heating`**|
|||**`20000 MJ`**|**`energy per fusion power cycle`**|

![](images/tmp2afbqpn1.pdf-0124-02.png)

![](images/tmp2afbqpn1.pdf-0124-03.png)

![](images/tmp2afbqpn1.pdf-0124-04.png)

![](images/tmp2afbqpn1.pdf-0129-06.png)

![](images/tmp2afbqpn1.pdf-0129-08.png)

![](images/tmp2afbqpn1.pdf-0130-04.png)

![](images/tmp2afbqpn1.pdf-0130-06.png)

![](images/tmp2afbqpn1.pdf-0130-07.png)

![](images/tmp2afbqpn1.pdf-0130-08.png)

![](images/tmp2afbqpn1.pdf-0154-04.png)

![](images/tmp2afbqpn1.pdf-0179-01.png)

![](images/tmp2afbqpn1.pdf-0179-02.png)

![](images/tmp2afbqpn1.pdf-0180-00.png)

![](images/tmp2afbqpn1.pdf-0182-00.png)

![](images/tmp2afbqpn1.pdf-0184-02.png)

|**`PUHPDOVN BETWEEN »U«HS`**|||
|---|---|---|
|**`plaaaa chiabtr V C I U M l«"-3)`**|**`(voluaa)`**|**`)1.S3S1`**|
|**`prasaura in piaiaa chaafcar aftar burn (Pa)`**|**`(pand)`**|**`0.219a»ff`**|
|**`piaiaura In piaiaa ehaabar bafora itart of burn`**|**`(Pa) (pstart)`**|**`».?i*a-»?`**|
|**`dwalt t l M batwaan b u m s (a)`**|**`(tdwall)`**|**`1 >•••><`**|
|**`r n u l r e d DT puap ipaad la")/»l`**|**`(1(21)`**|**`4.437/`**|
|**`OT spaed providad (a^3/i>`**|**`<anat(2>>`**|**`21.64S3`**|

|**(pdlv)**|**.l?»a»*f**|
|---|---|
|**(fha)**|**•.1271**|
|**(si 31>**|**Z9.C413**|
|**l i m t n i l **|**3 2 . I M 4**|

|**`(frata)`**|**`».714a-»5`**|
|---|---|
|**`1 a ( 4 > )`**|**`29.C4»3`**|
|**`hnrtlt))`**|**`29.(413`**|

![](images/tmp2afbqpn1.pdf-0188-00.png)

![](images/tmp2afbqpn1.pdf-0188-01.png)

![](images/tmp2afbqpn1.pdf-0189-00.png)

![](images/tmp2afbqpn1.pdf-0193-00.png)

![](images/tmp2afbqpn1.pdf-0193-01.png)

![](images/tmp2afbqpn1.pdf-0194-00.png)

![](images/tmp2afbqpn1.pdf-0194-01.png)

