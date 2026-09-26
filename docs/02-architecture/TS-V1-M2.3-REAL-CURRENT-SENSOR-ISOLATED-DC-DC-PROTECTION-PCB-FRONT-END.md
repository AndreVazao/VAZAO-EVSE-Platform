# VAZAO EVSE TestStation V1 — M2.3
# REAL CURRENT SENSOR + ISOLATED DC/DC + PROTECTION + PCB FRONT-END

Status: Engineering baseline — prototype selection, NOT production release
Repository: AndreVazao/VAZAO-EVSE-Platform
Branch: feat/charger-hardware-v1

## 1. Objective

M2.3 closes the main component-level decisions for the measurement front-end:
- real current sensor selection;
- isolated supply for the isolated voltage amplifiers;
- HV divider resistor architecture;
- input protection;
- CP/PP analogue front-end;
- contactor driver and feedback;
- PCB partition and first placement rules;
- creepage/clearance worksheet;
- calibration fixture BOM;
- verification procedure v0.2.

Target:
- 230/400 VAC;
- 50 Hz;
- 32 A/phase nominal;
- 22 kW maximum three-phase;
- Zone A and Zone B;
- three voltage channels + three current channels per zone;
- synchronized phase measurement;
- IEC 61851 CP/PP validation;
- electrically independent safety chain.

No component value in this document is a production safety approval without project-specific installation, fault-current, thermal, insulation and certification calculations.

## 2. Current-sensor decision

### 2.1 Requirements

Each phase current channel shall support:
- 0…32 A RMS continuous nominal operation;
- overload margin above nominal;
- AC waveform measurement at 50/60 Hz;
- sufficient bandwidth for transient and distortion diagnostics;
- low phase error;
- galvanic isolation between mains conductor and measurement electronics;
- low insertion loss;
- calibration capability;
- predictable thermal behaviour;
- production availability.

### 2.2 Candidates

#### Candidate A — TI TMCS1123

Preferred baseline for the first prototype.

Relevant manufacturer data:
- 80 A RMS continuous capability;
- reinforced isolation;
- 600 Vrms working isolation rating;
- 10 kV peak surge isolation rating;
- 250 kHz signal bandwidth;
- sensitivity error specification down to ±0.1%;
- non-linearity ±0.1%;
- operating supply 3.0–5.5 V;
- multiple sensitivity options;
- integrated overcurrent alert;
- 8.1 mm minimum creepage and clearance at device level.

Why preferred:
- 32 A is well inside the continuous capability;
- integrated isolation removes a separate isolation barrier for the current channel;
- bandwidth is more than adequate for 50 Hz phase measurement;
- low insertion loss is useful for a portable test instrument;
- external zero-current reference can simplify calibration.

Final sensitivity variant shall be selected after ADS131M06 input-range and overload calculations.

#### Candidate B — TI TMCS1133

Alternative where higher bandwidth is useful.

Relevant manufacturer data:
- 80 A RMS continuous capability;
- reinforced isolation;
- 600 Vrms working isolation;
- 10 kV peak surge isolation;
- 1 MHz bandwidth;
- sensitivity options approximately 20 mV/A to 150 mV/A;
- low conductor resistance;
- integrated overcurrent alert.

The 1 MHz bandwidth is not required for V1 50 Hz phase-angle measurement, so it remains an alternative.

#### Candidate C — LEM CDSR family

Technically interesting where compact AC/DC/leakage-current measurement is required.

The CDSR family specifies a 32 A RMS primary-current class, DC to 2 kHz bandwidth and 8 mm creepage/clearance, and is explicitly positioned for EV-charger applications.

It is not selected as the primary V1 phase-current sensor because the 32 A primary rating leaves less continuous overload margin than the 80 A TI alternatives.

### 2.3 Decision

V1 prototype baseline: TMCS1123 family, 80 A RMS class.

Selection rule:
- choose a sensitivity variant that keeps maximum expected current and transient below ADC limits;
- retain ADC headroom for overload diagnostics;
- perform one-time calibration against an independent reference meter;
- validate amplitude and phase error at 0.5 A, 1 A, 5 A, 10 A, 16 A, 24 A and 32 A;
- repeat at representative temperatures.

The sensor shall not be treated as the sole safety current detector.

## 3. Current-channel analogue path

Recommended topology:

PHASE CONDUCTOR -> TMCS1123 -> RC ANTI-ALIAS FILTER -> ADS131M06 -> STM32G474RE

The sensor is on the hazardous-side current path while its analogue output is isolated from the primary conductor by the sensor's internal isolation barrier.

The ADC input network shall be dimensioned from the selected TMCS1123 sensitivity variant.

Controls:
- differential ADC input;
- symmetrical RC network;
- short analogue routing;
- local decoupling;
- controlled analogue reference return;
- no shared high-current return path through measurement ground;
- dedicated test point for sensor output/reference.

## 4. Isolated DC/DC for AMC1311B

### 4.1 Requirement

Each AMC1311B high-side supply must be isolated from the low-side control/ADC domain unless a different certified isolated architecture is explicitly adopted.

TI documentation permits generating the high-side supply from the low-side supply with an isolated DC/DC architecture and also shows an SN6501 + transformer approach.

### 4.2 Prototype architecture

24 VDC CONTROL -> isolated DC/DC -> 5 V_ISO -> AMC1311B VDD1

One isolated supply may feed several voltage-sensing channels only if:
- its isolation barrier is appropriate for the complete group;
- channel-to-channel isolation requirements are respected;
- output power/noise is adequate;
- PCB creepage/clearance is maintained;
- common-mode transient behaviour is verified.

### 4.3 Candidate module

RECOM R05P205S/R05P205S class 5 V isolated DC/DC remains a candidate family only after checking exact current, isolation capacitance, creepage/clearance and safety approvals against the final AMC1311B supply architecture.

A second-source option shall be retained from Murata or an equivalent industrial reinforced-isolation family.

### 4.4 Selection checks

Do not choose the DC/DC solely by nominal output voltage.

Verify:
- insulation classification;
- working voltage;
- test voltage;
- isolation capacitance;
- creepage;
- clearance;
- output current;
- temperature derating;
- switching frequency;
- conducted/radiated noise;
- startup behaviour;
- short-circuit behaviour;
- lifecycle/availability.

### 4.5 AMC1311B local decoupling

Per TI reference guidance:
- 100 nF low-ESR ceramic close to VDD1/GND1;
- 1 uF low-ESR ceramic close to VDD1/GND1;
- 100 nF low-ESR ceramic close to VDD2/GND2;
- 1 uF low-ESR ceramic close to VDD2/GND2.

Effective capacitance under DC bias shall be checked.

## 5. Voltage-divider front-end

M2.2 established:
- 230 Vrms phase-to-neutral;
- Vpeak approximately 325.3 V;
- AMC1311B input target around 1.8 V peak;
- approximate divider ratio 0.00553;
- example 1.8 Mohm top resistance and 10 kohm bottom resistance.

M2.3 converts this into a PCB architecture rather than declaring the example values final.

### 5.1 Resistor string

Use multiple series HV resistors:

Lx -> RHV1 -> RHV2 -> RHV3 -> RHV4 -> RLOW -> AMC1311B input

Exact resistor count/value shall be selected from:
- individual resistor working voltage;
- pulse overload;
- creepage;
- voltage coefficient;
- tolerance;
- power rating;
- temperature coefficient;
- availability.

### 5.2 Preliminary target

For 1.8 Mohm total top resistance and 10 kohm bottom resistance:
- total = 1.81 Mohm;
- divider current at 230 Vrms approximately 127 uA;
- total resistor dissipation approximately 29 mW;
- bottom resistor voltage approximately 1.27 Vrms.

These values are starting points for simulation and tolerance analysis only.

### 5.3 Protection

Add a dedicated low-energy protection network around the AMC1311B input:
- series impedance;
- appropriate bidirectional/clamp protection;
- local filtering;
- controlled discharge path where required.

Evaluate:
- surge;
- EFT;
- ESD where applicable;
- mains transients;
- resistor-string failure modes.

## 6. Voltage-channel PCB architecture

Each voltage channel:
1. HV input connector/test point;
2. input protection;
3. resistor string;
4. RC filtering;
5. AMC1311B;
6. isolated DC/DC supply;
7. isolation boundary;
8. differential output filter;
9. ADS131M06 input.

Physical grouping:
- Zone A L1/L2/L3 adjacent;
- Zone B L1/L2/L3 adjacent;
- isolation barriers visually and physically obvious;
- no high-current load routing through precision measurement;
- ADC close to six conditioned differential outputs.

## 7. CP front-end — IEC 61851

The CP channel shall support:
- State A/B/C/D detection;
- PWM duty-cycle measurement;
- CP positive/negative excursion measurement;
- diode-state detection;
- open/short/fault simulation;
- controlled pilot generation for EV emulation.

Architecture:
MCU PWM -> controlled CP driver -> EVSE CP
EVSE CP -> protected divider/level shifter -> ADC/comparator -> MCU

CP input protection shall tolerate the expected ±12 V class pilot waveform and faults without exposing the MCU to out-of-range voltage.

Measured data:
- voltage;
- duty cycle;
- frequency;
- state;
- transition timing;
- abnormal amplitude;
- diode signature;
- fault condition.

## 8. PP front-end

PP shall support resistor-coded cable/current simulation according to the selected EVSE/IEC 61851 implementation.

Architecture:
PP connector -> protected measurement -> programmable resistance/simulation -> MCU

Modes:
- open;
- standard cable-current values;
- diagnostic resistance;
- fault/open-wire;
- charger interpretation verification.

The programmable resistance implementation shall fail safe and must not accidentally advertise a higher cable current than intended.

## 9. Contactor driver

Required topology:

Safety/MCU command -> protected transistor or driver -> 24 VDC contactor coil

Include:
- coil suppression;
- current-limited control;
- contactor auxiliary feedback;
- welded-contact detection;
- driver fault reporting.

A discrete low-side MOSFET stage is acceptable for prototype if VDS margin, coil current, gate resistor/pull-down, suppression and fault behaviour are engineered.

The safety chain must remove contactor coil power independently of normal software control.

## 10. Contactor feedback

Each safety-relevant contactor shall have auxiliary contact or equivalent certified feedback.

| Command | Feedback | Interpretation |
|---|---|---|
| OFF | OPEN | expected |
| OFF | CLOSED | possible welded contact |
| ON | CLOSED | expected |
| ON | OPEN | failure to close / coil / mechanism fault |

Software may identify the likely failure class, but the hardwired safety architecture shall not rely on software diagnosis to make the hazardous circuit safe.

## 11. HV protection baseline

Protection shall be coordinated, not simply duplicated.

Preliminary chain:

INPUT -> MAIN ISOLATOR -> SHORT-CIRCUIT PROTECTION -> SPD where applicable -> CONTACTOR -> ZONE/LOAD PROTECTION

Final protective device selection requires:
- installation supply type;
- prospective short-circuit current;
- upstream protection;
- conductor cross-section;
- cable length;
- ambient temperature;
- installation method;
- breaking capacity;
- selectivity;
- coordination;
- applicable local requirements.

The TestStation shall not assume that 32 A automatically determines a particular MCB/fuse rating.

## 12. Creepage / clearance worksheet v0.1

For every hazardous-to-SELV boundary record:
- working voltage;
- overvoltage category;
- pollution degree;
- insulation type;
- required creepage;
- required clearance;
- actual PCB value;
- slot/cutout use;
- package limitation;
- manufacturing tolerance.

The final value shall be taken from the applicable insulation standard and component certification, not a generic PCB spacing table.

Pay special attention to:
- AMC1311B barrier;
- TMCS1123 barrier;
- DC/DC barrier;
- CP/PE interfaces;
- mains connectors;
- relay/contactor isolation;
- PCB slots under isolation barriers.

## 13. PCB partition

### TS-MEASURE
ADS131M06, AMC1311B channels, current sensors, filters, references, calibration points and measurement MCU interface.

### TS-SAFE
Safety MCU, watchdog, E-stop input, contactor feedback, hardwired coil enable, thermal interlocks and fault latch.

### TS-EV
CP, PP, pilot generation, pilot measurement and fault injection.

### TS-LOAD
Load switching, load feedback, thermal sensors and fan control.

High-voltage load copper shall remain physically separated from precision measurement.

## 14. First PCB placement rules

Placement order:
1. isolation barriers;
2. mains/HV connectors;
3. current-sensor primary paths;
4. AMC1311B + isolated DC/DC;
5. ADS131M06;
6. voltage-divider strings;
7. analogue filters;
8. MCU;
9. safety circuitry;
10. communications;
11. test points.

Rules:
- current paths short and wide;
- no fast digital signals beneath analogue inputs;
- CP switching currents away from voltage measurement;
- controlled analogue return;
- safety and measurement grounds separated according to isolation architecture;
- slots where required to extend creepage;
- probe access to calibration nodes;
- hazardous areas marked on silkscreen/fabrication drawings.

## 15. Calibration fixture BOM v0.1

Required external equipment:
- calibrated three-phase voltage source or traceable reference;
- calibrated current source/load;
- precision reference multimeter;
- reference power analyser;
- oscilloscope with suitable isolated/differential probes;
- frequency reference;
- controlled-temperature method for engineering validation;
- phase-reference generator;
- safe breakout fixture for Zone A and Zone B;
- calibration harness.

The TestStation must not calibrate itself against its own unverified measurements.

## 16. Calibration points

Voltage:
- 0 V;
- 50 V;
- 120 V;
- 230 V RMS;
- controlled overrange test.

Current:
- 0 A;
- 0.5 A;
- 1 A;
- 5 A;
- 10 A;
- 16 A;
- 24 A;
- 32 A.

Phase:
- 0°;
- 30°;
- 60°;
- 90°;
- 120°;
- 150°;
- 180° where supported.

Three-phase operation shall validate 120° nominal relationships independently.

## 17. Verification procedure v0.2

### V0 — visual / continuity
- PCB inspection;
- isolation inspection;
- connector verification;
- PE continuity;
- no short between isolated domains.

### V1 — low voltage only
- 24 VDC power-up;
- current consumption;
- MCU boot;
- safety MCU boot;
- watchdog;
- communications;
- CP/PP electronics without mains.

### V2 — isolated measurement
- verify AMC1311B supplies;
- verify ADC baseline;
- verify zero-current offsets;
- verify isolated DC/DC temperature/noise;
- verify sensor reference.

### V3 — controlled voltage
Apply controlled low-voltage AC first.
Check RMS, frequency, phase, channel consistency, ADC clipping and protection.

### V4 — controlled current
Apply current progressively.
Check sensor linearity, thermal rise, ADC range, phase error, zero crossing and harmonic response.

### V5 — 230/400 V controlled energisation
Only after V0–V4 pass.
Check Zone A, Zone B, contactor feedback, E-stop, watchdog, load isolation and PE.

### V6 — EVSE protocol
Connect a controlled EVSE/EV emulator.
Check CP state A/B/C/D, PWM, PP, contactor timing, charging current, fault injection and report generation.

### V7 — long duration
Run representative load for 1 h, 4 h and extended thermal validation.
Log voltage, current, power, phase, temperature, sensor drift, contactor state and safety events.

## 18. Intelligent diagnosis data model

Every measurement event shall preserve:
1. raw measurement;
2. calibrated measurement;
3. uncertainty;
4. detected anomaly;
5. affected zone;
6. hypothesis;
7. confirmation test;
8. result;
9. recommended action.

Example:
Zone A phase angle normal -> Zone B phase angle abnormal.

The diagnosis must report an evidence chain, not an automatic declaration that a specific component is defective.

## 19. Phase-angle diagnostic rule

For each pair:
- L1-L2;
- L2-L3;
- L3-L1.

Calculate:
- measured phase;
- expected phase;
- absolute deviation;
- uncertainty;
- temperature;
- waveform quality;
- harmonic indicators.

Warning threshold shall be derived from:

threshold = measurement uncertainty + installation/EVSE acceptance requirement + engineering margin

No fixed universal 1° threshold shall be hard-coded.

## 20. Capacitor recommendation guardrail

If the diagnostic engine identifies a possible reactive-power/phase-displacement problem, it may calculate a candidate correction.

It shall never automatically command a physical capacitor connection.

The report must state:
- measured voltage;
- current;
- PF;
- phase displacement;
- frequency;
- calculated reactive power;
- target PF;
- calculated capacitor range;
- voltage rating;
- frequency;
- tolerance;
- switching duty;
- discharge requirements;
- harmonic/resonance risk;
- engineering validation requirement.

## 21. M2.3 BOM v0.4

| Ref | Function | Baseline | Status |
|---|---|---|---|
| U-MEAS-01..06 | isolated voltage sensing | TI AMC1311B family | SELECTED BASELINE |
| U-ADC-01 | 6-channel ADC | TI ADS131M06 | SELECTED BASELINE |
| U-MCU-01 | measurement MCU | STM32G474RE | SELECTED BASELINE |
| U-I-01..06 | isolated current sensing | TI TMCS1123 family | SELECTED BASELINE |
| U-DCISO-* | isolated DC/DC | RECOM/Murata 5 V class | CANDIDATE / HOLD |
| R-HV-* | HV divider string | multi-resistor HV architecture | HOLD |
| Q-DRV-* | contactor drivers | protected MOSFET stage | PROTOTYPE |
| K-MAIN | main contactor | 24 V industrial contactor | CANDIDATE |
| K-LOAD | load contactor | 24 V industrial contactor | CANDIDATE |
| J-CP | CP interface | protected service connector | PROTOTYPE |
| J-PP | PP interface | protected service connector | PROTOTYPE |
| F-* | branch protection | project-specific | HOLD |
| SPD-* | surge protection | project-specific | HOLD |
| PSU-24 | control supply | Phoenix Contact 24 V class | SELECTED FAMILY |
| MCU-SAFE | safety controller | STM32G0/G4 class | PROTOTYPE |
| CAN-ISO | isolated CAN | TI ISO1044 class | SELECTED BASELINE |

## 22. M2.3 acceptance criteria

M2.3 is complete when:
- current sensor baseline is selected;
- current accuracy/thermal test plan exists;
- isolated DC/DC architecture is defined;
- voltage divider is represented as a real resistor string;
- HV protection strategy exists;
- CP/PP component-level architecture exists;
- contactor driver and feedback architecture exists;
- PCB partition and placement rules exist;
- creepage/clearance worksheet exists;
- calibration fixture is defined;
- verification procedure v0.2 exists;
- unresolved production values are explicitly marked HOLD.

## 23. Next milestone — M2.4

M2.4 shall produce:
1. exact MPN freeze for current sensor;
2. exact isolated DC/DC MPN;
3. exact resistor part numbers;
4. input protection component selection;
5. CP/PP resistor/driver network;
6. contactor driver schematic;
7. complete TS-MEASURE schematic;
8. complete TS-SAFE schematic;
9. first PCB stack-up;
10. creepage/clearance drawing;
11. harness pinout;
12. prototype BOM with quantities;
13. manufacturing notes;
14. bring-up checklist;
15. measurement firmware data structure.

## Engineering references

The current-sensor baseline is based on manufacturer documentation for TI TMCS1123/TMCS1133, LEM CDSR and the AMC1311 family.

TI AMC1311 documentation explicitly describes using an isolated DC/DC converter to generate the high-side supply and specifies local 100 nF + 1 uF decoupling on each supply side.

All component choices remain subject to final safety, EMC, thermal, insulation, certification and availability review.
