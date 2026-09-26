# VAZAO EVSE TestStation V1 — M2.5
# COMPLETE SCHEMATIC RELEASE + PCB NET CLASSES + FIRST PLACEMENT

Status: Prototype schematic baseline — engineering review required before mains commissioning
Repository: AndreVazao/VAZAO-EVSE-Platform
Branch: feat/charger-hardware-v1

## 1. Purpose

M2.5 converts M2.4 into the first complete electrical schematic package.

This release defines:
- TS-MEASURE circuit sheets;
- TS-SAFE circuit sheets;
- TS-EV CP/PP architecture;
- contactor driver;
- protection placeholders and hold points;
- connector strategy;
- net classes;
- PCB keepouts;
- first placement;
- ERC/DRC rules;
- test-point map;
- firmware register/data map.

The design remains a prototype engineering baseline. No mains connection is authorized solely by this document.

## 2. Important metrology correction

The six AMC1311B channels require six independent isolated high-side supplies.

AMC1311B input-side supply current is in the mA range, and the device accepts 3.0–5.5 V on VDD1 in the B variant. TI specifies the input range as -0.1 V to 2 V. Therefore each isolated supply shall be dimensioned with sufficient continuous current and transient margin.

The MEJ1S2405SC 1 W / 5 V class converter is retained as the prototype candidate, but its exact continuous load, thermal rise and isolation capacitance must be verified before PCB release.

Reference: TI AMC1311 datasheet. citeturn0search48

## 3. Schematic sheet tree

The KiCad/EDA project shall use:

00-COVER-INDEX
01-POWER-INPUT
02-POWER-PROTECTION
03-ZONE-A
04-ZONE-B
05-CURRENT-SENSORS
06-VOLTAGE-SENSORS
07-ADC-MEASUREMENT-MCU
08-TS-SAFE
09-TS-CONTACTORS
10-TS-EV-CP
11-TS-EV-PP
12-TS-COMMS-CAN
13-24VDC
14-THERMAL-FANS
15-TEST-POINTS

## 4. Global electrical domains

HV-AC
HV-LOAD
PE
SELV-24V
SELV-3V3
MEAS-3V3
ISO-A1
ISO-A2
ISO-A3
ISO-B1
ISO-B2
ISO-B3
CP
PP
CAN-ISO
CAN-SERVICE

No net from an ISO-* domain may cross into another ISO-* domain without an explicitly documented isolation barrier.

## 5. TS-MEASURE — voltage channel

Six identical channels.

### Channel topology

Lx
-> FUSE/PROTECTION HOLD
-> RHV1
-> RHV2
-> RHV3
-> RHV4
-> RLOW
-> RIN
-> AMC1311B VIN

AMC1311B output:
OUTP/OUTN
-> differential RC
-> ADS131M06 CHx

High-side supply:
24V_CTRL
-> MEJ1S2405SC
-> 5V_ISO_x
-> TLV70033DCKR
-> 3V3_ISO_x
-> AMC1311B VDD1

Low-side:
3V3_MEAS -> AMC1311B VDD2.

### Voltage divider prototype values

RHV1..RHV4:
470 kOhm each.

RLOW:
10.0 kOhm, 1%.

RIN:
1.0 kOhm.

CIN:
4.7 nF.

These are prototype starting values and must be validated by tolerance, surge and frequency-response analysis.

## 6. TS-MEASURE — current channel

Six channels.

Topology:

PHASE CONDUCTOR
-> TMCS1123A3AQDVGR primary conductor
-> downstream circuit

TMCS1123 OUT
-> 47 Ohm series
-> ADS131M06 CHx

Differential capacitor:
4.7 nF prototype.

Optional common-mode capacitor:
DNP initially.

Reason for DNP:
common-mode capacitance can introduce phase/amplitude error and EMC current. Populate only after validation.

The TMCS1123 family is specified by TI for 80 ARMS continuous current and 250 kHz bandwidth, making the 32 A target comfortably inside the prototype operating envelope. The selected A3 variant is the 75 mV/A class. 

## 7. ADS131M06 channel assignment

ADC-01:

| Channel | Function |
|---|---|
| CH0 | Zone A L1 voltage |
| CH1 | Zone A L2 voltage |
| CH2 | Zone A L3 voltage |
| CH3 | Zone A L1 current |
| CH4 | Zone A L2 current |
| CH5 | Zone A L3 current |

ADC-02:

| Channel | Function |
|---|---|
| CH0 | Zone B L1 voltage |
| CH1 | Zone B L2 voltage |
| CH2 | Zone B L3 voltage |
| CH3 | Zone B L1 current |
| CH4 | Zone B L2 current |
| CH5 | Zone B L3 current |

This preserves synchronized six-channel acquisition inside each zone.

The ADS131M06 provides six simultaneously sampled differential inputs, up to 32 kSPS and programmable channel-to-channel phase calibration. citeturn0search0turn0search2

## 8. ADC clock and sampling baseline

Prototype:
- external low-jitter clock;
- target sample rate: 8 kSPS or 16 kSPS;
- 50 Hz fundamental;
- synchronized channels.

Final sample rate shall be selected after CPU load and anti-alias response are measured.

Phase processing shall use the same timestamp domain for voltage and current.

## 9. Measurement calculations

For each phase:

Vrms = sqrt(mean(v[n]^2))

Irms = sqrt(mean(i[n]^2))

P = mean(v[n] × i[n])

S = Vrms × Irms

PF = P / S

For phase:
phi = atan2(Q, P)

The implementation shall prefer synchronized waveform calculations over relying only on zero-crossing timing.

Phase calibration shall be stored independently for every voltage/current channel.

## 10. TS-SAFE

### Inputs

SAFE_ESTOP
SAFE_DOOR
SAFE_LOAD_OT
SAFE_POWER_FAULT
SAFE_WATCHDOG
KMAIN_FB
KLOAD_FB

### Outputs

KMAIN_ENABLE
KLOAD_ENABLE
FAN_ENABLE
SAFE_STATUS

### Safety logic

SAFE_OK =
E_STOP_OK
AND DOOR_OK
AND LOAD_TEMP_OK
AND POWER_OK
AND WATCHDOG_OK
AND INTERNAL_FAULT_CLEAR

KMAIN_ENABLE =
SAFE_OK AND MAIN_REQUEST

KLOAD_ENABLE =
SAFE_OK AND LOAD_REQUEST

The final physical E-stop circuit shall be capable of removing contactor coil energy independently of the application MCU.

## 11. Watchdog architecture

Two levels:

### MCU watchdog
STM32G031 internal watchdog.

### External hardware supervision
Independent timeout/enable mechanism shall remove the contactor-enable path if the heartbeat stops.

Heartbeat:
SAFE_HEARTBEAT

Nominal heartbeat:
10 ms period.

Timeout baseline:
100 ms.

The exact timeout is subject to safety hazard analysis and contactor release-time measurement.

## 12. Contactor driver

KMAIN:

24V_CTRL
-> contactor coil
-> QMAIN
-> SAFE_RETURN.

QMAIN:
logic-level N-MOSFET.

Gate:
MCU/SAFE output
-> 100 Ohm
-> gate.

Gate pulldown:
10 kOhm.

Suppression:
prototype TVS/flyback network selected for the exact LC1D32BD coil.

The suppression network shall be chosen to balance:
- coil release time;
- transistor stress;
- EMC;
- contactor release requirements.

## 13. Contactor feedback

KMAIN_FB and KLOAD_FB use mechanically linked auxiliary contacts.

Input path:

AUX_CONTACT
-> protected 24 V input
-> optically/electrically isolated digital input where required
-> SAFE MCU.

Fault matrix:

OFF + CLOSED = possible welded contact.
ON + OPEN = failure to close.
ON + CLOSED = normal.
OFF + OPEN = normal.

The diagnostic software may classify likely causes, but the safety layer must react to unsafe feedback independently.

## 14. TS-EV — CP

CP interface domains:

CP_HV_SIGNAL
CP_MEASURE
CP_DRIVER
CP_FAULT_INJECT

### CP measurement

EVSE CP
-> high-impedance protected divider
-> comparator/ADC
-> STM32.

The front end must accept the positive and negative pilot excursions without allowing the MCU pins to exceed their rated range.

### CP generation

STM32 PWM
-> CP driver
-> controlled pilot output.

The CP driver shall include:
- current limiting;
- fault-safe default;
- output disable;
- controlled positive/negative levels;
- fault injection switch.

No direct MCU GPIO shall be exposed at the external CP connector.

## 15. TS-EV — PP

PP topology:

PP connector
-> current-limited protection
-> selectable resistor bank
-> PP_RETURN.

Default state:
all resistance paths OPEN.

The resistor bank shall never default to a higher advertised cable-current capacity.

Firmware states:

PP_OPEN
PP_13A
PP_20A
PP_32A
PP_FAULT
PP_DIAGNOSTIC

The exact resistance values shall follow the selected IEC 61851 implementation and cable coding used by the VAZAO TestStation.

## 16. Power input sheet

Baseline:

L1/L2/L3
-> main isolator
-> short-circuit protection
-> SPD where required
-> KMAIN
-> Zone A / load distribution.

PE:
input PE
-> PE bar
-> chassis
-> TestStation exposed conductive parts
-> controlled measurement references as required.

N:
input neutral
-> protected neutral distribution
-> required measurement/load circuits.

The final protective devices require prospective short-circuit current, upstream protection, conductor data, installation method and applicable local requirements.

## 17. 24 VDC distribution

PSU-24:
QUINT4-PS/3AC/24DC/10, item 2904621.

Manufacturer data lists 24 V DC / 10 A nominal output, 240 W output power and short-circuit protection. citeturn0search1turn0search3

Branches:

F24-01 -> TS-SAFE
F24-02 -> TS-MEASURE isolated converters
F24-03 -> TS-EV
F24-04 -> contactors
F24-05 -> fans
F24-06 -> service/HMI
F24-07 -> spare

Each branch shall have independent protection and a measured current budget.

## 18. TS-COMMS

Primary bus:
CAN-FD.

Node IDs:

0x10 — Safety
0x20 — Measurement A
0x21 — Measurement B
0x30 — EV interface
0x40 — Load
0x50 — HMI/controller

Service:
USB/UART isolated or protected service interface.

CAN messages shall include:
- board ID;
- firmware version;
- hardware revision;
- heartbeat;
- fault flags;
- measurement status;
- calibration revision.

## 19. PCB net classes

### NET-HV-POWER
For mains/load conductors.

Rules:
- maximum current based on actual conductor/copper calculation;
- no routing through measurement PCB;
- dedicated creepage/clearance.

### NET-HV-MEASURE
For voltage divider input before isolation.

Rules:
- high-voltage spacing;
- resistor-string spacing;
- no low-voltage copper crossing;
- guarded physical area.

### NET-ISO
Each ISO-Ax/ISO-Bx is a separate class.

Rules:
- no shared copper between isolated islands;
- local ground only;
- no common plane crossing barriers.

### NET-ANALOGUE
Measurement outputs.

Rules:
- short;
- differential where applicable;
- away from clocks and switching nodes.

### NET-DIGITAL
MCU/SPI/CAN.

Rules:
- controlled return path;
- no crossing isolation barriers.

### NET-SAFE
Safety logic.

Rules:
- physically separated from high-noise switching;
- no dependence on application software for the final safe state.

## 20. PCB keepouts

Mandatory keepout polygons:

KO-HV-A
KO-HV-B
KO-ISO-A1
KO-ISO-A2
KO-ISO-A3
KO-ISO-B1
KO-ISO-B2
KO-ISO-B3
KO-CP
KO-PE

No copper pour, trace or via may enter an isolation keepout.

Creepage slots shall be used where required by the final insulation calculation.

## 21. First physical placement

### PCB-A TS-MEASURE

Left:
Zone A voltage/current sensor interfaces.

Centre:
six AMC1311B + six isolated supplies.

Right:
two ADS131M06.

Bottom:
STM32G474RE and reference/clock.

Top edge:
isolated service/CAN interface.

The six independent isolation islands shall be visually obvious.

### PCB-B TS-SAFE

Left:
external safety connectors.

Centre:
STM32G031K8T6 + watchdog/supervision.

Right:
contactor drivers.

Top:
feedback inputs.

Bottom:
safe-state outputs.

### PCB-C TS-EV

Left:
CP connector/protection.

Centre:
CP driver/measurement.

Right:
PP resistor bank.

Bottom:
fault-injection switches.

### PCB-D TS-POWER/LOAD

Physical DIN-rail/industrial layout rather than precision PCB-first architecture:
- isolator;
- protection;
- SPD;
- KMAIN;
- KLOAD;
- load switching;
- terminals;
- PE bar;
- fans/thermal.

## 22. Test-point map

TP01 — 24V_CTRL
TP02 — 3V3_MEAS
TP03 — 3V3_ISO_A1
TP04 — 3V3_ISO_A2
TP05 — 3V3_ISO_A3
TP06 — 3V3_ISO_B1
TP07 — 3V3_ISO_B2
TP08 — 3V3_ISO_B3
TP09 — AMC1311B A1 output
TP10 — AMC1311B B1 output
TP11 — TMCS1123 A1 output
TP12 — TMCS1123 B1 output
TP13 — ADC reference
TP14 — SAFE_STATUS
TP15 — KMAIN_FB
TP16 — KLOAD_FB
TP17 — CP_MEASURE
TP18 — PP_MEASURE
TP19 — CAN-H
TP20 — CAN-L

All test points shall be reachable without crossing hazardous areas during low-voltage bring-up.

## 23. ERC rules

ERC shall flag:
- unpowered MCU supply;
- floating safety input;
- unconnected contactor feedback;
- isolated domain with missing local supply;
- ADC input without defined bias/reference;
- CP external node directly connected to MCU;
- PP path with no fail-safe default;
- E-stop path dependent solely on MCU output.

Warnings may be waived only with a documented engineering reason.

## 24. DRC rules

DRC shall check:
- clearance by net class;
- creepage keepouts;
- minimum track width;
- minimum via diameter;
- annular ring;
- copper-to-edge;
- silkscreen-to-pad;
- differential pair constraints where used;
- isolation slot geometry.

HV rules shall be separate from SELV rules.

## 25. Firmware register/data map v0.1

### System
0x0000 DEVICE_ID
0x0004 HW_REV
0x0008 FW_REV
0x000C STATUS
0x0010 FAULT_FLAGS
0x0014 CAL_REV

### Measurement
0x0100 VA_L1
0x0104 VA_L2
0x0108 VA_L3
0x010C IA_L1
0x0110 IA_L2
0x0114 IA_L3
0x0118 POWER_L1
0x011C POWER_L2
0x0120 POWER_L3
0x0124 PF_L1
0x0128 PF_L2
0x012C PF_L3
0x0130 PHASE_L1_L2
0x0134 PHASE_L2_L3
0x0138 PHASE_L3_L1
0x013C FREQUENCY

### Safety
0x0200 SAFE_STATUS
0x0204 E_STOP
0x0208 DOOR
0x020C LOAD_OT
0x0210 KMAIN_FB
0x0214 KLOAD_FB
0x0218 WATCHDOG
0x021C SAFE_FAULT

### EV
0x0300 CP_STATE
0x0304 CP_VOLTAGE
0x0308 CP_PWM
0x030C PP_STATE
0x0310 PP_RESISTANCE
0x0314 EV_FAULT

### Load
0x0400 LOAD_REQUEST
0x0404 LOAD_SETPOINT
0x0408 LOAD_STATUS
0x040C LOAD_TEMP

## 26. Measurement packet v0.1

Every measurement frame shall contain:

timestamp
zone
phase
Vrms
Irms
P
Q
S
PF
phase_angle
frequency
THD_estimate
temperature
uncertainty
calibration_revision
fault_flags

Raw waveform capture shall be triggered by:
- phase anomaly;
- overcurrent;
- overvoltage;
- CP fault;
- contactor mismatch;
- thermal fault;
- operator diagnostic request.

## 27. First PCB manufacturing notes

Prototype boards shall use:
- 4-layer TS-MEASURE;
- 4-layer TS-SAFE;
- 2 or 4-layer TS-EV depending on final CP topology;
- DIN/terminal construction for TS-POWER/LOAD.

Measurement PCB:
- ENIG or equivalent prototype finish;
- controlled solder-mask openings around isolation slots;
- no exposed copper inside mandatory creepage paths;
- reference designators visible on service components.

## 28. Schematic release gates

Before ordering PCB-A:
1. verify every AMC1311B supply current against the isolated converter;
2. verify all resistor voltage ratings;
3. verify AMC1311B input maximum under worst-case mains;
4. verify ADS131M06 input range and gain;
5. verify TMCS1123 output at 32 A plus overload;
6. verify analogue filter phase delay;
7. verify creepage/clearance;
8. verify isolation capacitance;
9. ERC clean or documented waivers.

Before PCB-D mains assembly:
1. prospective fault current known;
2. protection breaking capacity known;
3. conductor sizing complete;
4. contactor utilization category verified;
5. PE continuity verified;
6. E-stop behaviour verified;
7. thermal/load calculations complete.

## 29. M2.5 exit criteria

M2.5 is complete when:
- complete schematic sheet tree exists;
- measurement channel assignment exists;
- safety logic exists;
- CP/PP architecture exists;
- contactor driver exists;
- PCB net classes exist;
- isolation keepouts exist;
- first placement exists;
- test-point map exists;
- firmware register/data map exists;
- engineering hold points are explicit.

## 30. Next milestone — M2.6

M2.6 shall turn this schematic baseline into a fabrication-oriented release:

1. exact CP resistor/driver MPNs;
2. exact PP resistor bank and switches;
3. exact MOSFET/suppression MPN;
4. exact input protection;
5. exact connectors;
6. complete capacitor/resistor BOM;
7. PCB stack-up and dimensions;
8. placement coordinates;
9. trace-width/current calculations;
10. thermal calculations;
11. isolation/creepage worksheet with actual values;
12. harness connector MPNs;
13. production-style BOM quantities;
14. assembly drawing;
15. prototype inspection checklist.

## References

TI ADS131M06 official product data confirms six simultaneous 24-bit channels, up to 32 kSPS and channel-to-channel phase calibration. citeturn0search0turn0search2

TI AMC1311 documentation confirms the 2 V high-impedance input and the 3.0–5.5 V AMC1311B high-side supply range. citeturn0search48

Phoenix Contact lists item 2904621 as a 24 V DC / 10 A QUINT4 supply with 240 W nominal output and short-circuit protection. citeturn0search1turn0search3

All prototype values remain subject to final electrical safety, EMC, thermal, insulation, short-circuit and certification review.
