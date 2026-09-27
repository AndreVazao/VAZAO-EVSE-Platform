# VAZAO EVSE TestStation V1 — M2.4
# MPN FREEZE + FIRST IMPLEMENTATION PACKAGE

Status: Prototype implementation baseline — engineering review required before mains commissioning
Repository: AndreVazao/VAZAO-EVSE-Platform
Branch: feat/charger-hardware-v1

## 1. Purpose

M2.4 converts the M2.3 architecture into a first implementation baseline with exact manufacturer part numbers where the engineering evidence is sufficient.

This is a prototype engineering release. It is not a declaration of compliance, certification or production approval.

Critical correction carried into M2.4:

Each AMC1311B voltage-sensing channel has its own isolated high-side supply.

The six AMC1311B input sides cannot share one floating high-side supply because the six phase measurement references must remain independent. Sharing that floating supply would unintentionally couple the measurement points.

Therefore:
- 3 x Zone A voltage channels = 3 independent isolated supplies;
- 3 x Zone B voltage channels = 3 independent isolated supplies;
- total = 6 isolated DC/DC channels.

This is now a mandatory architecture rule.

## 2. Exact core IC MPN freeze

### 2.1 Measurement ADC

U-ADC-01:
ADS131M06IPBSR

Texas Instruments:
- 6 differential simultaneously sampled channels;
- 24 bit;
- up to 32 kSPS;
- programmable gain;
- channel-to-channel phase calibration;
- 2.7 to 3.6 V supply;
- TQFP-32.

The selected package is TQFP for prototype assembly and inspection.

### 2.2 Voltage isolation amplifier

U-VA-01..06:
AMC1311BDWVR

Texas Instruments:
- 2 V high-impedance input;
- reinforced isolation;
- 5 kVrms isolation test rating;
- 1500 Vrms working isolation;
- 3.3 V high-side operation for AMC1311B;
- maximum AMC1311B offset ±1.5 mV;
- maximum gain error ±0.2%;
- -55 to +125 °C device range.

Use one device per voltage channel.

### 2.3 Current sensor

U-IA-01..06:
TMCS1123A3AQDVGR

Texas Instruments:
- 75 mV/A sensitivity;
- 80 ARMS continuous sensor class;
- 250 kHz bandwidth;
- reinforced isolation;
- 600 Vrms working isolation;
- 10 kV peak surge isolation;
- 3.0 to 5.5 V supply;
- 8.1 mm minimum creepage and clearance at device level;
- -40 to +125 °C.

The A3 variant is selected because 75 mV/A provides useful resolution while the device family supports the required bidirectional 32 A measurement range.

At 32 A:
VOUT nominal excursion = 32 A × 75 mV/A = 2.40 V peak.

The final ADC interface shall preserve headroom for offset, tolerance and transient conditions.

### 2.4 Measurement MCU

U-MCU-01:
STM32G474RET6

STMicroelectronics:
- Cortex-M4;
- up to 170 MHz;
- 512 KB Flash;
- 128 KB SRAM;
- industrial temperature range.

The MCU performs measurement acquisition, calibration, phase processing, diagnostics and communications. It is not the sole safety controller.

### 2.5 Safety MCU

U-SAFE-01:
STM32G031K8T6

Prototype safety-controller baseline.

The safety MCU supervises:
- E-stop;
- door/interlock;
- contactor feedback;
- load overtemperature;
- watchdog;
- safe-state request;
- fault latch.

The final safety integrity architecture remains subject to system hazard analysis.

### 2.6 Isolated CAN

U-CAN-01:
ISO1044BDWR

Texas Instruments isolated CAN transceiver baseline.

Use for the measurement/control bus where galvanic isolation is required.

## 3. Correct isolated voltage-supply architecture

### 3.1 Per-channel architecture

Each AMC1311B receives an independent isolated supply:

24V_CTRL -> isolated DC/DC -> 5V_ISO_x -> 3.3V_ISO_x -> AMC1311B VDD1

For x = A1, A2, A3, B1, B2, B3.

The 5 V isolated rail is locally regulated to 3.3 V.

### 3.2 Exact isolated converter

PS-ISO-A1..B3:
MEJ1S2405SC

Murata Power Solutions:
- 21.6 to 26.4 V input;
- 5 V output;
- 200 mA output class;
- 1 W;
- approximately 5.2 kV isolation class.

One module per AMC1311B channel.

This part is preferred over the previously mentioned R05P205S because R05P205S is a 5 V input module and is not a direct 24 V bus converter.

### 3.3 Local 3.3 V regulator

U-LDO-A1..B3:
TLV70033DCKR

Texas Instruments:
- fixed 3.3 V;
- 200 mA;
- SC70-5;
- low noise;
- low quiescent current.

Each isolated channel receives its own LDO.

### 3.4 Local decoupling

For each isolated voltage channel:

5V_ISO:
- C-ISO-IN = 1 uF ceramic;
- C-ISO-OUT = 1 uF ceramic.

3V3_ISO:
- C-LDO-IN = 100 nF;
- C-LDO-OUT = 1 uF.

AMC1311B:
- 100 nF close to each supply pair;
- 1 uF local bulk/decoupling.

Exact capacitor dielectric/package shall be selected during PCB BOM release.

## 4. Main 24 V supply

PSU-24:
QUINT4-PS/3AC/24DC/10
Order No. 2904621

Phoenix Contact.

Baseline:
- 3-phase input;
- 24 V DC;
- 10 A;
- 240 W class;
- DIN rail;
- SFB technology;
- monitoring/NFC functions.

The previous-generation item 2866705 is not the preferred new-design baseline because Phoenix Contact identifies 2904621 as the newer item for new projects.

The 24 V supply is intentionally oversized relative to expected control electronics so that contactor coils, fans, solenoids, isolated converters and control electronics have margin.

Actual total load shall be measured during prototype bring-up.

## 5. Current sensor supply

TMCS1123A3 devices operate from the common low-voltage measurement supply.

Baseline:
3V3_MEAS

No isolation is required between TMCS1123 output and ADS131M06 because the TMCS1123 itself provides galvanic isolation between the measured current conductor and its signal/control side.

Each sensor receives:
- 100 nF local ceramic;
- 1 uF local ceramic;
- optional ferrite/RC filtering if noise testing requires it.

Do not place a large common impedance in the six sensor supply paths.

## 6. Current-sensor ADC interface

For each channel:

TMCS1123 OUT -> RFI/anti-alias network -> ADS131M06 differential input

Initial prototype network:
- series R = 47 ohm;
- C differential = 4.7 nF;
- optional 1 nF common-mode capacitors only after EMC/phase-error validation.

The 47 ohm / 4.7 nF network is a prototype starting point, not a final metrology value.

The final network must be validated for:
- amplitude attenuation;
- phase delay;
- ADC stability;
- sensor output drive;
- common-mode behaviour.

The phase-delay contribution must be included in calibration.

## 7. Voltage-divider component baseline

### 7.1 Top resistor string

For each phase voltage channel:

Lx -> R1 -> R2 -> R3 -> R4 -> RLOW -> AMC1311B

Baseline R1..R4:
VR25000004703JA500

Vishay VR25:
- 470 kOhm;
- 5%;
- 0.25 W class;
- high-voltage resistor family.

Total top resistance:
4 × 470 kOhm = 1.88 MOhm

RLOW:
10.0 kOhm, 1%, 0.25 W minimum.

Preferred precision resistor family to be selected from the same qualified HV/low-voltage resistor vendor during BOM procurement.

### 7.2 Electrical estimate

At 230 Vrms:
Idiv = 230 / (1.88M + 10k) ≈ 121.7 uA RMS.

Voltage across RLOW:
VLOW ≈ 1.217 Vrms.

Peak voltage:
VLOW_peak ≈ 1.72 V.

At 253 Vrms (+10%):
VLOW_peak ≈ 1.89 V.

This leaves margin below the 2 V AMC1311B input limit in the nominal resistor-ratio calculation.

Tolerance, resistor voltage coefficient, temperature and surge behaviour must still be included in the final error budget.

### 7.3 Why four series resistors

Four resistors:
- distribute voltage stress;
- improve fault containment;
- allow physical spacing;
- simplify thermal/pulse analysis;
- improve creepage management.

Do not replace the four-resistor string with one resistor without engineering review.

## 8. RLOW protection and filtering

Initial channel:

RHV_STRING -> RLOW -> RIN -> AMC1311B IN

Prototype values:
- RLOW = 10.0 kOhm, 1%;
- RIN = 1.0 kOhm;
- C_IN = 4.7 nF.

The final cutoff and input impedance shall be checked against the AMC1311B input requirements.

Protection components shall be placed so that a failed upstream resistor does not expose the amplifier input to uncontrolled energy.

A low-energy clamp network may be populated after the surge/fault analysis determines the appropriate device.

## 9. CP component baseline

CP is a ±12 V-class IEC 61851 pilot interface.

The first implementation shall use:
- protected input divider;
- comparator/ADC monitoring;
- PWM output driver;
- fault injection switching;
- dedicated CP connector;
- PE reference handled according to the final EVSE interface architecture.

No direct MCU pin shall be connected to the CP connector.

The CP interface must withstand:
- normal pilot voltage;
- negative excursion;
- open circuit;
- short to PE;
- short to signal ground in controlled test modes;
- abnormal EVSE behaviour.

The exact resistor values and driver MPN will be frozen in the dedicated CP schematic release after the selected CP connector/reference architecture is fixed.

## 10. PP component baseline

PP uses a programmable resistor bank.

The bank shall be implemented as:

PP -> protection -> resistor selection -> PP_RETURN

The switching elements shall default to OPEN.

No reset, MCU failure or software crash may cause the TestStation to advertise a higher cable-current capability.

Initial resistor population shall support the cable-current values required by the selected IEC 61851 implementation.

The exact resistor bank will be released with the CP/PP schematic.

## 11. Contactor selection

Main contactor baseline:
LC1D32BD

Schneider Electric TeSys D:
- 3 poles;
- 32 A class;
- 24 V DC coil;
- AC-1/AC-3 application classes.

Use as the prototype baseline for the main 3-phase switching function.

Important:
The TestStation load path can reach 22 kW and the contactor selection must be validated for actual resistive/electronic load duty, switching frequency, ambient temperature and fault conditions. The 32 A label alone is not the complete selection criterion.

Auxiliary feedback:
- use mechanically linked auxiliary contact;
- one feedback channel per safety-relevant contactor;
- separate feedback from coil command.

## 12. Contactor driver

Prototype driver:
- Q-DRV = logic-level N-MOSFET;
- R-G = 100 ohm;
- R-GPD = 10 kOhm;
- flyback/suppression selected to actual contactor coil;
- gate controlled by safety-enable AND normal command.

Architecture:

24V -> K_COIL -> Q_DRV -> SAFE_RETURN

The safety chain shall interrupt the coil return or supply independently.

The final MOSFET MPN will be selected from:
- VDS >= 60 V;
- continuous current comfortably above coil current;
- low RDS(on) at available gate drive;
- avalanche/suppression compatibility;
- thermal margin.

## 13. Main safety chain

The following shall be hardwired as far as practical:

E_STOP -> SAFETY_LATCH -> CONTACTOR_ENABLE -> K_MAIN

Supervisory MCU signals may request safe shutdown but cannot defeat the E-stop.

Inputs:
- E_STOP;
- DOOR_INTERLOCK;
- LOAD_OVERTEMP;
- POWER_FAULT;
- WATCHDOG_FAULT;
- K_MAIN_FB;
- K_LOAD_FB.

Outputs:
- K_MAIN_ENABLE;
- K_LOAD_ENABLE;
- FAN_ENABLE;
- SAFE_STATUS.

A watchdog timeout shall force the safe state.

## 14. PCB stack-up — first baseline

Recommended 4-layer measurement/safety PCB:

L1:
- components;
- critical analogue;
- controlled short current-sensor signal paths.

L2:
- controlled low-voltage reference/ground zones;
- no hazardous copper crossing isolation barriers.

L3:
- power distribution;
- controlled digital routing where required.

L4:
- secondary signals;
- service/debug.

For the HV/load PCB, use a separate board rather than routing 22 kW copper through the precision measurement board.

This separation is mandatory for the first prototype unless a documented alternative is approved.

## 15. Board partition

### PCB-A — TS-MEASURE

Contains:
- 6 × AMC1311B;
- 6 × isolated DC/DC;
- 6 × TLV70033;
- 6 × TMCS1123;
- ADS131M06;
- STM32G474RE;
- references;
- analogue filtering;
- calibration points.

### PCB-B — TS-SAFE

Contains:
- STM32G031K8T6;
- E-stop logic;
- watchdog;
- contactor drivers;
- feedback inputs;
- thermal interlocks;
- safety status.

### PCB-C — TS-EV

Contains:
- CP;
- PP;
- PWM generation;
- CP state measurement;
- PP resistor bank;
- controlled fault injection.

### PCB-D — TS-POWER/LOAD

Contains:
- mains terminals;
- protection;
- contactors;
- load switching;
- load monitoring;
- thermal sensors;
- fans.

This four-board architecture is the preferred V1 prototype.

## 16. Harness pinout baseline

### H-MEASURE-A

| Pin | Signal |
|---|---|
| 1 | VA_L1 |
| 2 | VA_L2 |
| 3 | VA_L3 |
| 4 | IA_L1 |
| 5 | IA_L2 |
| 6 | IA_L3 |
| 7 | PE / shield reference as defined |
| 8 | shield |

### H-MEASURE-B

| Pin | Signal |
|---|---|
| 1 | VB_L1 |
| 2 | VB_L2 |
| 3 | VB_L3 |
| 4 | IB_L1 |
| 5 | IB_L2 |
| 6 | IB_L3 |
| 7 | PE / shield reference as defined |
| 8 | shield |

### H-SAFE

| Pin | Signal |
|---|---|
| 1 | E_STOP |
| 2 | DOOR_INTERLOCK |
| 3 | LOAD_OVERTEMP |
| 4 | K_MAIN_FB |
| 5 | K_LOAD_FB |
| 6 | WATCHDOG_HEARTBEAT |
| 7 | SAFE_STATUS |
| 8 | 0V_SAFE |

### H-EV

| Pin | Signal |
|---|---|
| 1 | CP |
| 2 | PP |
| 3 | PE/reference |
| 4 | CP_FAULT |
| 5 | PP_FAULT |
| 6 | CP_PWM |
| 7 | EV_STATUS |
| 8 | shield |

Final connector families shall be selected based on voltage/current category and serviceability.

## 17. Creepage/clearance implementation rules

The PCB library shall contain explicit keepout regions:
- HV-A;
- HV-B;
- ISO-A1;
- ISO-A2;
- ISO-A3;
- ISO-B1;
- ISO-B2;
- ISO-B3;
- SELV.

No copper pour may cross an isolation barrier.

No via may bridge a creepage slot.

The isolation barrier of every AMC1311B, MEJ1S2405SC and TMCS1123 shall follow the component manufacturer's certified dimensions and the applicable system insulation requirement.

## 18. Calibration architecture

### Voltage calibration

For each of six channels:
- zero/offset;
- gain;
- phase.

### Current calibration

For each of six channels:
- zero;
- gain;
- phase.

### Three-phase calibration

Use one independent traceable reference.

The reference shall provide:
- L1;
- L2;
- L3;
- controlled phase displacement;
- known RMS voltage/current.

Calibration records:
- serial number;
- board revision;
- sensor lot;
- calibration date;
- reference instrument;
- ambient temperature;
- coefficients;
- uncertainty;
- operator.

## 19. First firmware measurement object

Measurement packet fields:
- timestamp;
- sample_rate;
- zone;
- phase;
- voltage_rms;
- current_rms;
- real_power;
- apparent_power;
- reactive_power;
- power_factor;
- phase_angle_deg;
- frequency_hz;
- thd_estimate;
- sensor_temperature;
- measurement_uncertainty;
- calibration_revision;
- fault_flags.

Raw synchronized samples shall be retained for diagnostic events.

## 20. PCB bring-up sequence

### Stage 1
No mains.
Verify continuity, isolation, 24 V input, 3.3 V logic and each 3.3 V isolated supply one by one.

### Stage 2
Verify every AMC1311B channel independently.

### Stage 3
Verify every TMCS1123 channel using zero-current and controlled-current tests.

### Stage 4
Verify ADS131M06 simultaneous sampling.

### Stage 5
Verify phase-calibration algorithm using an external reference.

### Stage 6
Verify safety board and contactors without load.

### Stage 7
Verify CP/PP without connecting a vehicle.

### Stage 8
Controlled mains energisation through protected laboratory setup.

### Stage 9
Controlled EVSE connection.

### Stage 10
Full TestStation sequence.

## 21. M2.4 prototype BOM

| Ref | MPN / family | Qty prototype | Status |
|---|---|---:|---|
| U-ADC-01 | ADS131M06IPBSR | 2 | FROZEN |
| U-VA-01..06 | AMC1311BDWVR | 6 | FROZEN |
| U-IA-01..06 | TMCS1123A3AQDVGR | 6 | FROZEN |
| U-MCU-01 | STM32G474RET6 | 2 | FROZEN |
| U-SAFE-01 | STM32G031K8T6 | 2 | PROTOTYPE BASELINE |
| U-CAN-01 | ISO1044BDWR | 2 | FROZEN BASELINE |
| PS-ISO-A1..B3 | MEJ1S2405SC | 6 | FROZEN |
| U-LDO-A1..B3 | TLV70033DCKR | 6 | FROZEN |
| PSU-24 | QUINT4-PS/3AC/24DC/10, 2904621 | 1 | FROZEN |
| K-MAIN | LC1D32BD | 1 | PROTOTYPE BASELINE |
| R-HV-01..24 | VR25000004703JA500 | 24 | PROTOTYPE |
| R-LOW-01..06 | 10 kOhm 1% 0.25 W | 6 | HOLD MPN |
| R-IN-01..06 | 1 kOhm 1% | 6 | PROTOTYPE |
| C-IN-01..06 | 4.7 nF | 6 | PROTOTYPE |
| C-ISO-* | 1 uF / 100 nF ceramic | as required | PROTOTYPE |
| Q-DRV-* | logic-level N-MOSFET | 4+ | HOLD MPN |
| CP-* | IEC 61851 front-end | 1 set | HOLD |
| PP-* | programmable resistor bank | 1 set | HOLD |
| F-* | protection | project-specific | HOLD |
| SPD-* | surge protection | project-specific | HOLD |

The BOM deliberately marks unresolved safety-critical values as HOLD rather than inventing a false freeze.

## 22. Engineering change from M2.3

M2.3 listed an isolated 5 V DC/DC candidate that was not directly compatible with the 24 V control bus.

M2.4 corrects this by adopting:

24 V -> MEJ1S2405SC -> 5 V isolated -> TLV70033 -> 3.3 V isolated

and, critically:

ONE ISOLATED SUPPLY PER AMC1311B VOLTAGE CHANNEL.

This correction is required to preserve independent floating references for L1/L2/L3 in both Zone A and Zone B.

## 23. Current sensor evidence

TI currently lists TMCS1123 as active and specifies:
- 80 ARMS continuous current capability;
- 250 kHz bandwidth;
- reinforced isolation;
- 600 Vrms working isolation;
- 10 kV peak surge isolation;
- 3 to 5.5 V supply;
- multiple sensitivities including 75 mV/A.

The exact selected orderable part is TMCS1123A3AQDVGR.

The device is currently shown as active, although distributor/TI availability may vary. Procurement must therefore include a second-source strategy before production release.

## 24. M2.4 exit criteria

M2.4 is complete when:
- exact core MPNs are documented;
- six independent AMC1311B isolated supplies are implemented in the architecture;
- first four-board PCB partition is defined;
- harness pinout exists;
- current sensor sensitivity is frozen for prototype;
- voltage divider values have a quantitative operating-point calculation;
- contactor prototype baseline is defined;
- bring-up sequence exists;
- firmware measurement object exists;
- unresolved protection/CP/PP/driver items are explicitly HOLD.

## 25. Next milestone — M2.5

M2.5 shall produce the actual schematic release package:
1. TS-MEASURE complete circuit sheets;
2. TS-SAFE complete circuit sheets;
3. TS-EV CP schematic;
4. TS-EV PP schematic;
5. contactor driver schematic;
6. exact MOSFET and suppression selection;
7. exact RLOW MPN;
8. exact protection devices;
9. complete connector MPNs;
10. PCB net classes;
11. PCB keepouts;
12. first physical placement;
13. ERC/DRC rules;
14. complete prototype BOM;
15. assembly notes;
16. test-point map;
17. first firmware register/data map.

## 26. References used for component freeze

Manufacturer data reviewed for this release includes:
- TI TMCS1123;
- TI AMC1311/AMC1311B;
- TI ADS131M06;
- TI TLV70033;
- Murata MEJ1 series;
- Phoenix Contact QUINT4 2904621;
- Schneider Electric LC1D32BD;
- Vishay VR25.

All production values remain subject to electrical safety, EMC, thermal, insulation, short-circuit and certification review.
